import { Injectable } from '@angular/core';

export interface LocationOption {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

export interface ReverseGeocodingResult {
  osmId: number;
  displayName?: string;
  city: string;
  state: string;
  country: string;
}

export type LocationProvider = 'google' | 'nominatim';

@Injectable({
  providedIn: 'root'
})
export abstract class LocationSelectorService {
  abstract searchLocations(country: string, state: string, locality: string): Promise<LocationOption[]>;
  abstract reverseGeocode(latitude: number, longitude: number): Promise<ReverseGeocodingResult>;
  abstract locationProviderName: LocationProvider;
}
