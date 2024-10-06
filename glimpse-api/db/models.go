package db

import (
	"time"

	"gorm.io/gorm"
)

// Event defines model for Event.
type Event struct {
	gorm.Model
	// Description A description of the event.
	Description string `json:"description"`

	// Timestamp The time the event occurred.
	Timestamp      time.Time       `json:"timestamp"`
	Transcriptions []Transcription `json:"transcriptions,omitempty" gorm:"many2many:event_transcriptions;"`
	Location
}

// Location defines model for Location.
type Location struct {
	gorm.Model
	// Latitude Latitude of the location.
	Latitude float32 `json:"latitude,omitempty"`

	// Longitude Longitude of the location.
	Longitude float32 `json:"longitude,omitempty"`

	// Text The written address that corresponds to the coordinates.
	Text string `json:"text,omitempty"`
}

// Transcription defines model for Transcription.
type Transcription struct {
	gorm.Model
	// Audio The path to the original recording.
	Audio string `json:"audio"`

	// Content The content of the transcription.
	Content string `json:"content"`

	// Timestamp The time the transcription was created.
	Timestamp time.Time `json:"timestamp"`
}
