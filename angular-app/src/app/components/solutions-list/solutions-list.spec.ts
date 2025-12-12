import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SolutionsList } from './solutions-list';

describe('SolutionsList', () => {
  let component: SolutionsList;
  let fixture: ComponentFixture<SolutionsList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SolutionsList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SolutionsList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
