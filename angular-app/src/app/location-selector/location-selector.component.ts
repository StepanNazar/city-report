import {Component, signal, inject} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {LocationService} from '../location-service';
import {Country} from '../country';
import {State} from '../state';
import {Locality} from '../locality';

@Component({
  selector: 'app-location-selector',
  imports: [FormsModule],
  templateUrl: './location-selector.component.html',
  styleUrl: './location-selector.component.scss'
})
export class LocationSelector {
  countries: Country[] = [];
  states: State[] = [];
  localities: Locality[] = [];
  locationService: LocationService = inject(LocationService);

  readonly selectedCountry = signal<Country | null>(null);
  readonly selectedState = signal<State | null>(null);
  readonly selectedLocality = signal<Locality | null>(null);
  readonly selectStateDisabled = signal(true);
  readonly selectLocalityDisabled = signal(true);

  previousCountry: Country | null = null;
  previousState: State | null = null;

  constructor() {
    this.locationService.getCountries().then(
      (countries: Country[]) => {
        this.countries = countries;
      }
    );
  }

  onCountrySelect() {
    const country = this.selectedCountry();
    if (!country || this.previousCountry === country) return;

    this.selectedState.set(null);
    this.selectedLocality.set(null);
    this.selectStateDisabled.set(false);
    this.selectLocalityDisabled.set(true);

    this.previousCountry = this.selectedCountry();
    this.previousState = null;

    this.locationService.getStates(country.id).then(
      (states: State[]) => {
        this.states = states;
    });
  }

  onStateSelect() {
    const state = this.selectedState();
    if (!state || this.previousState === state) return;

    this.selectedLocality.set(null);
    this.selectLocalityDisabled.set(false);

    this.previousState = this.selectedState();

    this.locationService.getLocalities(state.id).then(
      (localities: Locality[]) => {
        this.localities = localities;
      }
    );
  }
}
