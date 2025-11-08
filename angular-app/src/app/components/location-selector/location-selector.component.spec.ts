import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LocationSelector } from './location-selector.component';

describe('LocalitySelector', () => {
  let component: LocationSelector;
  let fixture: ComponentFixture<LocationSelector>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LocationSelector]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LocationSelector);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
