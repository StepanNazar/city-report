import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PublicStats } from './public-stats';

describe('PublicStats', () => {
  let component: PublicStats;
  let fixture: ComponentFixture<PublicStats>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PublicStats]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PublicStats);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
