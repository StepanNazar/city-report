import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostEdit } from './post-edit';

describe('PostEdit', () => {
  let component: PostEdit;
  let fixture: ComponentFixture<PostEdit>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostEdit]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostEdit);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
