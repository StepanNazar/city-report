import { Injectable } from '@angular/core';

export interface LocationOption {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

export interface ReverseGeocodingResult {
  placeId: number;
  name: string;
  displayName: string;
  latitude: number;
  longitude: number;
  address: {
    road?: string;
    suburb?: string;
    city?: string;
    county?: string;
    state?: string;
    country?: string;
    postcode?: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export abstract class LocationSelectorService {
  abstract searchLocations(country: string, state: string, locality: string): Promise<LocationOption[]>;
  abstract reverseGeocode(latitude: number, longitude: number): Promise<ReverseGeocodingResult>;
  abstract getLocationProviderName(): string;
}
