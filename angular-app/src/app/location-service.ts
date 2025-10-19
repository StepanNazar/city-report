import { Injectable } from '@angular/core';
import {Country} from './country';
import {State} from './state';
import {Locality} from './locality';
@Injectable({
  providedIn: 'root'
})
export class LocationService{
  async getCountries(): Promise<Country[]> {
    const data = await fetch('http://localhost:5000/countries');
    return ((await data.json())["items"]) ?? [];
}
  async getStates(countryId: number): Promise<State[]> {
    const data = await fetch(`http://localhost:5000/countries/${countryId}/states`);
    return ((await data.json())["items"]) ?? [];
  }
  async getLocalities(stateId: number): Promise<Locality[]> {
    const data = await fetch(`http://localhost:5000/states/${stateId}/localities`);
    return ((await data.json())["items"]) ?? [];
  }
}
