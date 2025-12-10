import { Component } from '@angular/core';
import { PostFilterSearchPanel } from '../../components/post-filter-search-panel/post-filter-search-panel';
import { MapComponent } from '../../components/map/map.component';
import { ShortPostInfo } from '../../components/short-post-info/short-post-info';

@Component({
  selector: 'app-homepage',
  imports: [PostFilterSearchPanel, MapComponent, ShortPostInfo],
  templateUrl: './homepage.html',
  styleUrl: './homepage.scss'
})
export class Homepage {

}
