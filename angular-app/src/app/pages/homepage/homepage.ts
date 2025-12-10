import { Component, signal } from '@angular/core';
import { PostFilterSearchPanel } from '../../components/post-filter-search-panel/post-filter-search-panel';
import { MapComponent } from '../../components/map/map.component';
import { PostsList } from '../../components/posts-list/posts-list';
import { LocationOption } from '../../services/location-selector-service';

@Component({
  selector: 'app-homepage',
  imports: [PostFilterSearchPanel, MapComponent, PostsList],
  templateUrl: './homepage.html',
  styleUrl: './homepage.scss'
})
export class Homepage {
  readonly selectedLocation = signal<LocationOption | null>(null);
  readonly sortBy = signal<string>('created_at');
  readonly order = signal<string>('desc');

  onLocationSelected(location: LocationOption | null) {
    this.selectedLocation.set(location);
  }

  onSortByChanged(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.sortBy.set(value);
  }

  onOrderChanged(event: Event) {
    const value = (event.target as HTMLSelectElement).value;
    this.order.set(value);
  }
}
