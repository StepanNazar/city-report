import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportDetails } from './report-details';

describe('ReportDetails', () => {
  let component: ReportDetails;
  let fixture: ComponentFixture<ReportDetails>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportDetails]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReportDetails);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
