import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationChoiceComponent } from './location-choice-component';

describe('LocationChoiceComponent', () => {
  let component: LocationChoiceComponent;
  let fixture: ComponentFixture<LocationChoiceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LocationChoiceComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LocationChoiceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
