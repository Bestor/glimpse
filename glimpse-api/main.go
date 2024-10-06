package main

import (
	"encoding/json"
	"net/http"

	"log"

	"github.com/Bestor/glimpseapi/api"
	"github.com/Bestor/glimpseapi/db"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func initDB() (*gorm.DB, error) {
	database, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		return nil, err
	}

	// Auto-migrate the schema
	err = database.AutoMigrate(&db.Transcription{}, &db.Event{}, &db.Location{})
	if err != nil {
		return nil, err
	}

	return database, nil
}

type Server struct {
	DB *gorm.DB
}

// Handler for GET /transcriptions
func (s *Server) GetTranscriptions(w http.ResponseWriter, r *http.Request) {
	var transcriptions []db.Transcription
	result := s.DB.Find(&transcriptions)
	if result.Error != nil {
		http.Error(w, result.Error.Error(), http.StatusInternalServerError)
		return
	}

	apiTranscriptions := make([]api.Transcription, len(transcriptions))
	for i, transcription := range transcriptions {

		apiTranscription := api.Transcription{
			Audio:     transcription.Audio,
			Content:   transcription.Content,
			Timestamp: transcription.Timestamp,
		}
		apiTranscriptions[i] = apiTranscription
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(transcriptions); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// Handler for POST /transcriptions
func (s *Server) AddTranscription(w http.ResponseWriter, r *http.Request) {
	var transcription api.Transcription
	if err := json.NewDecoder(r.Body).Decode(&transcription); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	dbTranscription := db.Transcription{
		Audio:     transcription.Audio,
		Content:   transcription.Content,
		Timestamp: transcription.Timestamp,
	}

	result := s.DB.Create(&dbTranscription)
	if result.Error != nil {
		http.Error(w, result.Error.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(transcription)
}

// Handler for GET /events
func (s *Server) GetEvents(w http.ResponseWriter, r *http.Request) {
	var events []db.Event
	result := s.DB.Preload("Transcriptions").Find(&events)
	if result.Error != nil {
		http.Error(w, result.Error.Error(), http.StatusInternalServerError)
		return
	}

	apiEvents := make([]api.Event, len(events))
	for _, event := range events {
		eventID := uint32(event.ID)
		apiEvent := api.Event{
			Id:             &eventID,
			Description:    event.Description,
			Timestamp:      event.Timestamp,
			Transcriptions: &[]api.Transcription{},
			Location: &api.Location{
				Latitude:  &event.Location.Latitude,
				Longitude: &event.Location.Longitude,
				Text:      &event.Location.Text,
			},
		}

		transcriptionList := []api.Transcription{}

		for _, transcription := range event.Transcriptions {
			apiTranscription := api.Transcription{
				Audio:     transcription.Audio,
				Content:   transcription.Content,
				Timestamp: transcription.Timestamp,
			}
			transcriptionList = append(transcriptionList, apiTranscription)
		}
		*apiEvent.Transcriptions = transcriptionList
		apiEvents = append(apiEvents, apiEvent)
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(apiEvents); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// Handler for POST /events
func (s *Server) AddEvent(w http.ResponseWriter, r *http.Request) {
	var event api.Event
	if err := json.NewDecoder(r.Body).Decode(&event); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	var location db.Location
	if event.Location == nil {
		location = db.Location{}
	} else {
		location = db.Location{
			Latitude:  *event.Location.Latitude,
			Longitude: *event.Location.Longitude,
			Text:      *event.Location.Text,
		}
	}
	dbEvent := db.Event{
		Description:    event.Description,
		Timestamp:      event.Timestamp,
		Transcriptions: []db.Transcription{},
		Location:       location,
	}
	for _, transcription := range *event.Transcriptions {
		dbEvent.Transcriptions = append(dbEvent.Transcriptions, db.Transcription{
			Audio:     transcription.Audio,
			Content:   transcription.Content,
			Timestamp: transcription.Timestamp,
		})
	}

	result := s.DB.Create(&dbEvent)
	if result.Error != nil {
		http.Error(w, result.Error.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(event)
}

func main() {
	db, err := initDB()
	if err != nil {
		log.Fatal("failed to connect database:", err)
	}

	server := &Server{DB: db}

	mux := http.NewServeMux()
	mux.HandleFunc("/transcriptions", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			server.GetTranscriptions(w, r)
		case http.MethodPost:
			server.AddTranscription(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	mux.HandleFunc("/events", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			server.GetEvents(w, r)
		case http.MethodPost:
			server.AddEvent(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	log.Println("Server starting on :8080")
	log.Fatal(http.ListenAndServe(":8080", mux))
}
