import {Injectable} from '@angular/core';
import {LocationOption} from './location-option';
import {LocationSelectorService} from './location-selector-service';

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
}
