import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AIComment } from './aicomment';

describe('AIComment', () => {
  let component: AIComment;
  let fixture: ComponentFixture<AIComment>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AIComment]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AIComment);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
