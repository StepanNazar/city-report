import { Component, output, signal, effect, input, AfterViewInit, OnDestroy, ElementRef, viewChild } from '@angular/core';
import * as L from 'leaflet';

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

  readonly mapContainer = viewChild<ElementRef>('mapContainer');
  readonly coordinates = signal<Coordinates | null>(null);
  readonly coordinatesSelected = output<Coordinates>();
  readonly initialCoordinates = input<Coordinates | null>(null);

  constructor() {
    // When initial coordinates are provided (from location selector), update the map
    effect(() => {
      const initial = this.initialCoordinates();
      if (initial && this.map) {
        this.setMapCenter(initial.latitude, initial.longitude);
        this.coordinates.set(initial);
      }
    });
  }

  ngAfterViewInit() {
    // Initialize map after view is ready
    setTimeout(() => {
      this.initMap();
    }, 0);
  }

  ngOnDestroy() {
    if (this.map) {
      this.map.remove();
    }
  }

  private initMap() {
    const container = this.mapContainer()?.nativeElement;
    if (!container) {
      console.error('Map container not found');
      return;
    }

    // Default center (can be changed based on user location)
    const defaultLat = 50.4501;
    const defaultLng = 30.5234; // Kyiv coordinates

    try {
      this.map = L.map(container).setView([defaultLat, defaultLng], 13);
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

    // Set initial coordinates if provided
    const initial = this.initialCoordinates();
    if (initial) {
      this.setMapCenter(initial.latitude, initial.longitude);
    }
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

    this.map.setView([lat, lng], 15);
    this.addOrUpdateMarker(lat, lng);
  }
}
