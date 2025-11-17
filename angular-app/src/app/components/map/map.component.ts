import {
  afterNextRender,
  Component,
  ElementRef,
  inject,
  input,
  OnDestroy,
  output,
  signal,
  viewChild
} from '@angular/core';
import * as L from 'leaflet';
import {Coordinates, GeolocationService} from '../../services/geolocation.service';

@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent implements OnDestroy {
  private readonly DEFAULT_ZOOM = 13;
  private readonly MAX_ZOOM = 19;
  private readonly COORDINATE_PRECISION = 6;
  private readonly DEFAULT_ICON = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
    iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  private map?: L.Map;
  private marker?: L.Marker;
  private geolocationService = inject(GeolocationService);
  private mapClickHandler?: (e: L.LeafletMouseEvent) => void;

  readonly mapContainer = viewChild<ElementRef>('mapContainer');
  readonly mapError = signal<string | null>(null);
  readonly coordinates = signal<Coordinates | null>(null);
  readonly coordinatesSelected = output<Coordinates>();
  readonly initialCoordinates = input<Coordinates | null>(null);

  constructor() {
    // Note: initialCoordinates are only used once during map initialization
    // They do NOT update the map after initial load
    afterNextRender(async () => {
      await this.initMap();
    });
  }

  ngOnDestroy() {
    if (this.map) {
      if (this.mapClickHandler) this.map.off('click', this.mapClickHandler);
      this.map.remove();
    }
  }

  private async initMap() {
    const container = this.mapContainer()?.nativeElement;
    if (!container) {
      console.error('Map container not found');
      return;
    }

    let userCoords: Coordinates;
    const initial = this.initialCoordinates();
    if (initial) {
      userCoords = initial;
    } else {
      userCoords = await this.geolocationService.getCurrentCoordinates();
    }

    try {
      this.map = L.map(container).setView([userCoords.latitude, userCoords.longitude], this.DEFAULT_ZOOM);
    } catch (error) {
      this.mapError.set('Failed to initialize map');
      console.error('Error initializing map:', error);
      return;
    }

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: this.MAX_ZOOM
    }).addTo(this.map);

    // Add click event to map
    this.mapClickHandler = (e: L.LeafletMouseEvent) => {
      this.onMapClick(e.latlng.lat, e.latlng.lng);
    }
    this.map.on('click', this.mapClickHandler);
  }

  private onMapClick(lat: number, lng: number) {
    const newCoords: Coordinates = {
      latitude: Number(lat.toFixed(this.COORDINATE_PRECISION)),
      longitude: Number(lng.toFixed(this.COORDINATE_PRECISION))
    };

    this.coordinates.set(newCoords);
    this.addOrUpdateMarker(lat, lng);
    this.setMapCenter(lat, lng);
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
      icon: this.DEFAULT_ICON
    }).addTo(this.map);
  }

  private setMapCenter(lat: number, lng: number) {
    if (!this.map) return;
    this.map.setView([lat, lng]);
  }
}
