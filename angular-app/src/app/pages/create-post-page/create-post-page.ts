import { Component } from '@angular/core';
import { LocationChoiceComponent } from '../../components/location-choice-component/location-choice-component';
import { Map } from '../../components/map/map';
import { ImageUpload } from '../../components/image-upload/image-upload';

@Component({
  selector: 'app-create-post-page',
  imports: [LocationChoiceComponent, Map, ImageUpload],
  templateUrl: './create-post-page.html',
  styleUrl: './create-post-page.scss'
})
export class CreatePostPage {

}
