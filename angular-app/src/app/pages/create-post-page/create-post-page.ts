import { Component } from '@angular/core';
import { LocationSelector } from '../../components/location-selector/location-selector.component';
import { Map } from '../../components/map/map';
import { ImageUpload } from '../../components/image-upload/image-upload';

@Component({
  selector: 'app-create-post-page',
  imports: [LocationSelector, Map, ImageUpload],
  templateUrl: './create-post-page.html',
  styleUrl: './create-post-page.scss'
})
export class CreatePostPage {

}
