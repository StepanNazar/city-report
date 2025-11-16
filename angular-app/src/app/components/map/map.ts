import { Component, output, signal, input, AfterViewInit, OnDestroy, ElementRef, viewChild, inject } from '@angular/core';
import * as L from 'leaflet';
import { GeolocationService } from '../../services/geolocation.service';

export interface Coordinates {
  latitude: number;
  longitude: number;
}

@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.html',
  styleUrl: './map.scss'
})
export class Map implements AfterViewInit, OnDestroy {
  private map?: L.Map;
  private marker?: L.Marker;
  private geolocationService = inject(GeolocationService);

  readonly mapContainer = viewChild<ElementRef>('mapContainer');
  readonly coordinates = signal<Coordinates | null>(null);
  readonly coordinatesSelected = output<Coordinates>();
  readonly initialCoordinates = input<Coordinates | null>(null);
  readonly isLoadingLocation = signal<boolean>(false);

  constructor() {
    // Note: initialCoordinates are only used once during map initialization
    // They do NOT update the map after initial load
  }

  async ngAfterViewInit() {
    // Initialize map after view is ready
    setTimeout(async () => {
      await this.initMap();
    }, 0);
  }

  ngOnDestroy() {
    if (this.map) {
      this.map.remove();
    }
  }

  private async initMap() {
    const container = this.mapContainer()?.nativeElement;
    if (!container) {
      console.error('Map container not found');
      return;
    }

    // Get user location or use default (Kyiv)
    this.isLoadingLocation.set(true);
    let userCoords: Coordinates;

    // Check if initial coordinates are provided
    const initial = this.initialCoordinates();
    if (initial) {
      userCoords = initial;
    } else {
      userCoords = await this.geolocationService.getCurrentCoordinates();
    }
    this.isLoadingLocation.set(false);

    try {
      this.map = L.map(container).setView([userCoords.latitude, userCoords.longitude], 13);
    } catch (error) {
      console.error('Error initializing map:', error);
      return;
    }

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19
    }).addTo(this.map);

    // Add click event to map
    this.map.on('click', (e: L.LeafletMouseEvent) => {
      this.onMapClick(e.latlng.lat, e.latlng.lng);
    });
  }

  private onMapClick(lat: number, lng: number) {
    const newCoords: Coordinates = {
      latitude: Number(lat.toFixed(6)),
      longitude: Number(lng.toFixed(6))
    };

    this.coordinates.set(newCoords);
    this.addOrUpdateMarker(lat, lng);
    this.coordinatesSelected.emit(newCoords);
  }

  private addOrUpdateMarker(lat: number, lng: number) {
    if (!this.map) return;

    // Remove existing marker if any
    if (this.marker) {
      this.marker.remove();
    }

    // Add new marker
    this.marker = L.marker([lat, lng], {
      icon: L.icon({
        iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
        iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    }).addTo(this.map);
  }

  private setMapCenter(lat: number, lng: number) {
    if (!this.map) return;

    this.map.setView([lat, lng]);
    this.addOrUpdateMarker(lat, lng);
  }
}
