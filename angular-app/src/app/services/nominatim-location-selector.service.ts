import { Injectable } from '@angular/core';
import { LocationOption, LocationSelectorService, ReverseGeocodingResult } from './location-selector-service';

@Injectable({
  providedIn: 'root'
})
export class NominatimLocationSelectorService implements LocationSelectorService {
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
    const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&addressdetails=1`;
    const response = await fetch(url);
    const data = await response.json();

    return {
      placeId: data.place_id,
      name: data.name || data.display_name,
      displayName: data.display_name,
      latitude: parseFloat(data.lat),
      longitude: parseFloat(data.lon),
      address: {
        road: data.address?.road,
        suburb: data.address?.suburb,
        city: data.address?.city || data.address?.town || data.address?.village,
        county: data.address?.county,
        state: data.address?.state,
        country: data.address?.country,
        postcode: data.address?.postcode
      }
    };
  }

  getLocationProviderName(): string {
    return 'nominatim';
  }
}
