import {
  afterNextRender,
  Component,
  DestroyRef,
  ElementRef,
  inject,
  input,
  OnDestroy,
  output,
  signal,
  viewChild
} from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';
import { EMPTY, Subject } from 'rxjs';
import { debounceTime, switchMap } from 'rxjs/operators';
import * as L from 'leaflet';
import { Coordinates, GeolocationService } from '../../services/geolocation.service';
import { MapClusterItem, MapItem, MapPostItem, PostsService } from '../../services/posts.service';

@Component({
  selector: 'app-map',
  imports: [],
  templateUrl: './map.component.html',
  styleUrl: './map.component.scss'
})
export class MapComponent implements OnDestroy {
  // used for initial map settings before getting user location
  private readonly PREVIEW_COORDS: Coordinates = { latitude: 50.4501, longitude: 30.5234 };
  private readonly PREVIEW_ZOOM = 2;

  private readonly DEFAULT_ZOOM = 13;
  private readonly MAX_ZOOM = 19;
  private readonly COORDINATE_PRECISION = 6;
  private readonly DEBOUNCE_MS = 500;

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
  private markersLayer?: L.LayerGroup;
  private geolocationService = inject(GeolocationService);
  private postsService = inject(PostsService);
  private router = inject(Router);
  private destroyRef = inject(DestroyRef);
  private mapClickHandler?: (e: L.LeafletMouseEvent) => void;
  private mapMoveHandler?: () => void;

  // Subject for debouncing map moves in clusters mode
  private mapMoveSubject = new Subject<void>();

  readonly mapContainer = viewChild<ElementRef>('mapContainer');
  readonly mapError = signal<string | null>(null);
  readonly coordinates = signal<Coordinates | null>(null);
  readonly coordinatesSelected = output<Coordinates>();
  readonly initialCoordinates = input<Coordinates | null>(null);

  // Mode: 'picker' for selecting coordinates, 'clusters' for displaying post clusters
  readonly mode = input<'picker' | 'clusters'>('picker');

  constructor() {
    // Note: initialCoordinates are only used once during map initialization
    // They do NOT update the map after initial load
    afterNextRender(async () => {
      await this.initMap();
    });

    this.mapMoveSubject.pipe(
      debounceTime(this.DEBOUNCE_MS),
      switchMap(() => {
        if (!this.map || this.mode() !== 'clusters') {
          return EMPTY;
        }
        const bounds = this.map.getBounds();
        const zoom = this.map.getZoom();
        return this.postsService.getMapClusters(
          bounds.getSouth(),
          bounds.getNorth(),
          bounds.getWest(),
          bounds.getEast(),
          zoom
        );
      }),
      takeUntilDestroyed(this.destroyRef)
    ).subscribe({
      next: (response) => {
        if (response && response.items) {
          this.renderMapItems(response.items);
        }
      },
      error: (error) => {
        console.error('Error loading map clusters:', error);
      }
    });
  }

  ngOnDestroy() {
    if (this.map) {
      if (this.mapClickHandler) this.map.off('click', this.mapClickHandler);
      if (this.mapMoveHandler) this.map.off('moveend', this.mapMoveHandler);
      this.map.remove();
    }
  }

  private async initMap() {
    const container = this.mapContainer()?.nativeElement;
    if (!container) {
      console.error('Map container not found');
      return;
    }

    // Use initial coordinates if provided, otherwise use default coordinates to show map immediately
    const initialCoordinates = this.initialCoordinates();
    const coordinates: Coordinates = initialCoordinates || this.PREVIEW_COORDS;

    try {
      // Initialize map immediately with default/initial coordinates
      this.map = L.map(container).setView([coordinates.latitude, coordinates.longitude], this.PREVIEW_ZOOM);
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

    if (this.mode() === 'picker') {
      this.setupPickerMode();
    } else {
      this.setupClustersMode();
    }

    // If no initial coordinates were provided, get user coordinates asynchronously and update map
    if (!initialCoordinates) {
      await this.getUserCoordinatesAndUpdateMap();
    }
  }

  private setupPickerMode() {
    if (!this.map) return;

    this.mapClickHandler = (e: L.LeafletMouseEvent) => {
      this.onMapClick(e.latlng.lat, e.latlng.lng);
    };
    this.map.on('click', this.mapClickHandler);
  }

  private setupClustersMode() {
    if (!this.map) return;

    this.markersLayer = L.layerGroup().addTo(this.map);

    this.mapMoveHandler = () => {
      this.mapMoveSubject.next();
    };
    this.map.on('moveend', this.mapMoveHandler);
    this.mapMoveSubject.next();
  }

  private renderMapItems(items: MapItem[]) {
    if (!this.map || !this.markersLayer) return;
    this.markersLayer.clearLayers();
    for (const item of items) {
      if (item.type === 'post') {
        this.addPostMarker(item);
      } else {
        this.addClusterMarker(item);
      }
    }
  }

  private addPostMarker(item: MapPostItem) {
    if (!this.markersLayer) return;

    const marker = L.marker([item.latitude, item.longitude], {
      icon: this.DEFAULT_ICON
    });

    const popupContent = this.createPostPopupContent(item);
    marker.bindPopup(popupContent, {
      maxWidth: 280,
      className: 'post-popup'
    });

    marker.addTo(this.markersLayer);
  }

  private createPostPopupContent(item: MapPostItem): HTMLElement {
    const container = document.createElement('div');
    container.className = 'map-post-popup';

    if (item.thumbnailUrl) {
      const img = document.createElement('img');
      img.src = item.thumbnailUrl;
      img.alt = item.title;
      img.className = 'popup-thumbnail';
      container.appendChild(img);
    }

    const titleLink = document.createElement('a');
    titleLink.href = `/post/${item.id}`;
    titleLink.className = 'popup-title';
    titleLink.textContent = item.title;
    titleLink.addEventListener('click', (e) => {
      e.preventDefault();
      this.router.navigate(['/post', item.id]);
    });
    container.appendChild(titleLink);

    if (item.authorFirstName || item.authorLastName) {
      const author = document.createElement('div');
      author.className = 'popup-author';
      author.textContent = `${item.authorFirstName || ''} ${item.authorLastName || ''}`.trim();
      container.appendChild(author);
    }

    if (item.createdAt) {
      const date = document.createElement('div');
      date.className = 'popup-date';
      date.textContent = new Date(item.createdAt).toLocaleDateString();
      container.appendChild(date);
    }

    return container;
  }

  private addClusterMarker(item: MapClusterItem) {
    if (!this.markersLayer || !this.map) return;

    const sizeClass = this.getClusterSizeClass(item.count);
    const clusterIcon = L.divIcon({
      className: `cluster-icon ${sizeClass}`,
      html: `<span>${item.count}</span>`,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });

    const marker = L.marker([item.latitude, item.longitude], {
      icon: clusterIcon
    });

    marker.on('click', () => {
      this.map?.fitBounds([
        [item.bounds.minLat, item.bounds.minLng],
        [item.bounds.maxLat, item.bounds.maxLng]
      ], { padding: [20, 20] });
    });

    marker.addTo(this.markersLayer);
  }

  private getClusterSizeClass(count: number): string {
    if (count < 10) return 'cluster-small';
    if (count <= 50) return 'cluster-medium';
    return 'cluster-large';
  }

  private async getUserCoordinatesAndUpdateMap() {
    try {
      const userCoords = await this.geolocationService.getCurrentCoordinates();
      if (this.map) {
        this.map.setView([userCoords.latitude, userCoords.longitude], this.DEFAULT_ZOOM);
      }
    } catch (error) {
      console.warn('Could not get user coordinates, keeping default location:', error);
    }
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
