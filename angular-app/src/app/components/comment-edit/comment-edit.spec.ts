import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CommentEdit } from './comment-edit';

describe('CommentEdit', () => {
  let component: CommentEdit;
  let fixture: ComponentFixture<CommentEdit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CommentEdit]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CommentEdit);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
