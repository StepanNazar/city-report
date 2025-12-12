import { Component, output } from '@angular/core';
import { LocationSelector } from '../location-selector/location-selector.component';
import { LocationOption } from '../../services/location-selector-service';

@Component({
  selector: 'app-post-filter-search-panel',
  imports: [LocationSelector],
  templateUrl: './post-filter-search-panel.html',
  styleUrl: './post-filter-search-panel.scss'
})
export class PostFilterSearchPanel {
  readonly locationSelectedEvent = output<LocationOption | null>();
  readonly sortByChanged = output<Event>();
  readonly orderChanged = output<Event>();
}
