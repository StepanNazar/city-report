import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SolutionEdit } from './solution-edit';

describe('SolutionEdit', () => {
  let component: SolutionEdit;
  let fixture: ComponentFixture<SolutionEdit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SolutionEdit]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SolutionEdit);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
