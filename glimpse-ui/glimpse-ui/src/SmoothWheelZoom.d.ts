import * as L from "leaflet";

declare module "leaflet" {
    interface MapOptions {
        smoothWheelZoom?: boolean | string;
        smoothSensitivity?: number;
    }

    interface Map {
        smoothWheelZoom: boolean | string;
        smoothSensitivity: number;
    }

    namespace Map {
        interface SmoothWheelZoom extends Handler {
            addHooks(): void;
            removeHooks(): void;
            _onWheelScroll(event: WheelEvent): void;
        }
    }
}