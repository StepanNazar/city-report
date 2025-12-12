import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostPin } from './post-pin';

describe('PostPin', () => {
  let component: PostPin;
  let fixture: ComponentFixture<PostPin>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostPin]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostPin);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
