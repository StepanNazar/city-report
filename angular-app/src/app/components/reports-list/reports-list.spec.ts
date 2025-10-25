import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReportsList } from './reports-list';

describe('ReportsList', () => {
  let component: ReportsList;
  let fixture: ComponentFixture<ReportsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReportsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ReportsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
