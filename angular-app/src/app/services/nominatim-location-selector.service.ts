import { Injectable } from '@angular/core';
import {
  LocationOption,
  LocationProvider,
  LocationSelectorService,
  ReverseGeocodingResult
} from './location-selector-service';

@Injectable({
  providedIn: 'root'
})
export class NominatimLocationSelectorService implements LocationSelectorService {
  locationProviderName: LocationProvider = 'nominatim';

  async searchLocations(country: string, state: string, locality: string): Promise<LocationOption[]> {
    const url = `https://nominatim.openstreetmap.org/search?city=${locality}&country=${country}&state=${state}&format=geocodejson&featureType=settlement`;
    const response = await fetch(url);
    const data = await response.json();
    return data.features.map((feature: any) => {
      return {
        id: feature.properties.geocoding.osm_id,
        name: feature.properties.geocoding.label,
        latitude: feature.geometry.coordinates[1],
        longitude: feature.geometry.coordinates[0],
      };
    });
  }

  async reverseGeocode(latitude: number, longitude: number): Promise<ReverseGeocodingResult> {
    const url = `https://nominatim.openstreetmap.org/reverse?format=geocodejson&lat=${latitude}&lon=${longitude}`;
    const response = await fetch(url);
    const data = await response.json();

    const feature = data.features?.[0];
    if (!feature) {
      throw new Error('No results found for the given coordinates');
    }

    const geocoding = feature.properties.geocoding;

    return {
      osmId: geocoding.osm_id,
      displayName: geocoding.label,
      city: geocoding.city,
      state: geocoding.state || '',
      country: geocoding.country || '',
    };
  }
}
