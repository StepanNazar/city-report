import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PostFilterSearchPanel } from './post-filter-search-panel';

describe('PostFilterSearchPanel', () => {
  let component: PostFilterSearchPanel;
  let fixture: ComponentFixture<PostFilterSearchPanel>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PostFilterSearchPanel]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PostFilterSearchPanel);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
