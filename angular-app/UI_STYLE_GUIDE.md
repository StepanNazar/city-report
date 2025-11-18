# City Report – General Styling Guide

This styling guide defines the universal visual language, patterns, and design rules that ensure every newly created page remains visually consistent, readable, and aligned with the overall identity of the platform.

**Platform Purpose:** City Report is a civic engagement platform where community members report and discuss urban issues—such as broken street lights, road damage, deteriorating playgrounds, and other infrastructure problems—on an interactive map. The design should convey trust, clarity, and civic responsibility while remaining accessible to all community members.

**Core Design Values:**

- **Clarity:** Issues must be easy to report and understand
- **Accessibility:** Usable by diverse community members of all technical skill levels
- **Trust:** Professional appearance that inspires confidence in civic action
- **Efficiency:** Streamlined workflows that respect users' time

This guide focuses on global principles that apply across all pages and features.

______________________________________________________________________

## 1. Visual Identity

### 1.1 Color System

The color palette is designed to inspire trust and civic action while maintaining excellent readability and accessibility. Colors communicate status, priority, and feedback throughout the issue reporting workflow.

#### Primary Colors

- **Primary Accent:** `#1A83C5` — A trustworthy, professional blue used for primary actions (submit reports, confirm changes), interactive map elements, and critical UI components.
- **Primary Accent (Hover):** `#1570A8` — Darker shade for hover states, providing clear interactive feedback.
- **Primary Accent (Active/Pressed):** `#125D8F` — Darkest shade for pressed states, confirming user interaction.
- **Brand Blue (Titles):** `#1A6FB8` — Used for main headings and branding, slightly warmer to feel approachable.

#### Success & Resolution States

- **Success Color:** `#21A654` — A vibrant green indicating resolved issues, approved solutions, positive feedback, and completed actions.
- **Success Color (Hover/Active):** `#1A8443` — Darker green for interactive success elements.
- **Success Light Background:** `#E6F7EC` — Light green for success messages and resolved issue indicators.

#### Text Colors

- **Neutral Dark Text:** `#1C1C1C` / `#1E2530` / `#333333` — Primary text for maximum readability. Used for issue descriptions, comments, and main content.
- **Neutral Medium Text:** `#404040` / `#5C6470` / `#7A7A7A` — Secondary text for metadata (dates, usernames, vote counts), labels, and supporting information.
- **Neutral Light Text:** `#9EA3A9` / `#9AA2AF` — Muted text for placeholders, helper text, and low-priority information.

#### Borders & Surfaces

- **Light Border Tone:** `#E1E5E9` / `#E1E5EB` — Subtle borders for cards, inputs, and dividers. Creates structure without visual noise.
- **Subtle Border:** `rgba(0, 0, 0, 0.08)` — Very light border for elevated cards with shadows.
- **Surface White:** `#FFFFFF` — Clean background for issue cards, forms, and content panels.
- **App Background:** `#F7F8FA` — Soft grey background providing gentle contrast and reducing eye strain during extended use.
- **Tab Background:** `#F3F5F8` — Light grey for inactive tabs and secondary surfaces.

#### Status & Feedback Colors

- **Error/Danger:** `#E03E3E` / `#D9534F` — Red for form validation errors, failed actions, and critical issues requiring attention.
- **Error Light Background:** `#FEE2E2` — Light red background for error messages.
- **Warning Background:** `#FFFBEB` — Light yellow for warnings, notices, and moderate-priority alerts.
- **Warning Border:** `#FDE68A` — Yellow border for warning containers.
- **Warning Text:** `#92400E` — Dark amber for warning text content.

**Color Usage Guidelines:**

- Use primary blue sparingly—reserve for critical actions like "Submit Report" or "Post Comment"
- Success green indicates issue resolution and positive community actions
- Maintain WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
- Test colors in different lighting conditions and on various devices

All UI elements should derive colors from this palette to maintain consistent visual hierarchy and brand cohesion.

______________________________________________________________________

## 2. Typography System

### 2.1 Font Family

Use a clean, modern sans-serif font family that maintains good readability across platforms:

```
-apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Inter, "Helvetica Neue", Arial, sans-serif
```

All textual elements should inherit this base font.

### 2.2 Text Hierarchy

A clear typographic scale ensures readability and structured information flow:

- **Primary Heading:** `32px`, bold (700), used for top-level page titles
- **Secondary Heading:** `22px`, semi-bold (600), used for subsections and grouped content areas
- **Tertiary Heading:** `18px`, semi-bold (600), for less prominent titles or nested sections
- **Subtitle/Description:** `16px`, regular (400), for supporting text under headings
- **Body Text:** `15px`, regular (400), standard-size text used for general content, descriptions, and paragraphs
- **Label Text:** `14px`, medium (500), compact text used for form labels, field descriptions, and compact elements
- **Meta Text:** `13px`, regular (400), smaller muted text for timestamps, auxiliary notes, contextual descriptors, and subtle details
- **Small Text:** `12px`, for very compact information

### 2.3 Font Weights

- **Regular:** 400 — Default for body text
- **Medium:** 500 — For labels and subtle emphasis
- **Semi-Bold:** 600 — For headings and important text
- **Bold:** 700 — For primary headings and strong emphasis

Typography should maintain comfortable line spacing, emphasize clarity, and rely on weight rather than color alone for hierarchy.

______________________________________________________________________

## 3. Layout & Spacing

### 3.1 Spacing Rhythm

Consistent spacing creates visual rhythm and makes the interface predictable and scannable—essential when users are quickly browsing multiple issue reports or reading through community discussions.

**Recommended Scale:**

- **Micro:** 2-4px — Tight internal spacing (e.g., icon-to-text gaps, tab padding)
- **Small:** 6-8px — Between closely related elements (e.g., label to input)
- **Base:** 12-16px — Standard component spacing (e.g., between form fields, paragraph breaks)
- **Medium:** 20-24px — Section spacing (e.g., between card elements, comment separations)
- **Large:** 32-40px — Major block separation (e.g., between page sections)
- **XL:** 48px+ — Page-level structural spacing (e.g., between major content areas)

**Key Principles:**

- Related items should be closer together than unrelated items
- Increased spacing indicates decreased relationship
- Consistent spacing helps users scan and process information quickly
- White space is intentional—it reduces cognitive load

### 3.2 Page Layout

Pages balance information density with readability:

**Content-Focused Pages** (Issue details, post views):

- Centered layout with max-width container (typically 900-1200px)
- Generous side padding (24-40px) to prevent edge-to-edge content
- Vertical spacing separates logical sections

**Map-Integrated Pages** (Browse issues, location selection):

- Flexible layouts that accommodate map panels
- Responsive breakpoints to show/hide map on mobile
- Clear visual hierarchy between map and list views

**Form Pages** (Create report, add comment):

- Narrower max-width (600-900px) for comfortable reading and input
- Increased vertical spacing between form sections
- Clear visual progression through multi-step flows

### 3.3 Surface Structure

Typical page anatomy:

- **Navigation Bar** — Global header with branding, main navigation, and user controls
- **Main Content Area** — Primary content with cards, lists, or forms
- **Map Panel** (when applicable) — Interactive map showing issue locations
- **Sidebar/Filters** (when applicable) — Secondary controls and information

These elements maintain predictable spacing and avoid crowding, creating clear visual zones that help users navigate complex information.

______________________________________________________________________

## 4. Surfaces, Cards & Elevation

### 4.1 Card Elements

Cards and surface blocks share these common traits:

- **Background:** White (`#FFFFFF`)
- **Border Radius:** 6-12px (inputs/buttons use 6-7px, containers use 10-12px)
- **Border:** Either:
  - `1px solid #E1E5E9` for standard cards, OR
  - `1px solid rgba(0, 0, 0, 0.08)` for cards with shadow elevation
- **Shadow (Optional):** `0 4px 20px rgba(0, 0, 0, 0.05)` for elevated surfaces
  - Use sparingly and purposefully
  - Lighter shadows preferred: `0 2px 8px rgba(0, 0, 0, 0.04)` for subtle elevation

**Border Radius Scale:**

- **Small:** 6px — Input fields, small buttons
- **Medium:** 7-8px — Standard buttons, tabs
- **Large:** 10-12px — Cards, containers, panels
- **Extra Large:** 14px — Large containers
- **Pill:** 999px / 50% — Rounded pills and badges

Variation in elevation should be used sparingly and purposefully.

### 4.2 Container Padding

Internal padding should be generous, using medium or large spacing steps to support readable content blocks without clutter.

### 4.3 Dividers

Thin, neutral-colored dividers separate logical sections within containers. These should be subtle and not visually dominant.

- Standard: `1px solid #E1E5E9`
- Very subtle: `1px solid rgba(0, 0, 0, 0.05)`

______________________________________________________________________

## 5. Interactive Elements

### 5.1 Buttons

Buttons communicate action priority through visual weight. In a civic platform, clear calls-to-action are essential for encouraging community participation.

**Button Hierarchy:**

- **Primary Button:** Reserved for high-priority actions that advance the user's main goal

  - Background: `#1A83C5` (primary blue)
  - Text: White, 16px, semi-bold (600)
  - Border radius: 7px
  - Height: 50px minimum
  - Padding: Generous horizontal padding (e.g., `0 32px`)
  - Hover: `#1570A8` (darker blue)
  - Active: `#125D8F` (darkest blue)
  - Transition: `background 0.2s ease`
  - **Use for:** "Submit Report", "Post Comment", "Save Changes", "Create Account"

- **Secondary Button:** Supporting actions that don't disrupt the main flow

  - Border: `1px solid #E1E5E9`
  - Background: White or transparent
  - Text: Neutral dark color (`#404040`)
  - Same height and border radius as primary
  - Hover: Light grey background
  - **Use for:** "Cancel", "Go Back", "View Details", "Filter"

- **Minimal Button:** Low-priority or repetitive actions

  - Text-based with no border or background
  - Transparent background
  - Hover: Subtle background change (`#F7F8FA`)
  - Smaller padding
  - **Use for:** "Edit", "Delete", navigation links in lists

- **Danger Button:** Destructive or irreversible actions

  - Background: `#E03E3E` (red) or outlined red
  - Clear visual warning
  - **Use for:** "Delete Report", "Remove Comment"

- **Tab Buttons (Segmented Control):**

  - Container: `#F3F5F8` background, 2px padding, 7px border radius
  - Height: 44px
  - Inactive: Transparent background, `#7A7A7A` text, medium weight (500)
  - Active: White background, `#1C1C1C` text, 6px border radius
  - Transition: `all 0.2s ease`
  - **Use for:** View toggles, filtering between states (e.g., "All Issues" / "My Reports")

**Button Guidelines:**

- Use only one primary button per screen section
- Button text should be action-oriented ("Submit Report" not "Submit")
- Maintain minimum 44px touch targets for mobile accessibility
- Disabled buttons reduce opacity to 0.5-0.6 and show `not-allowed` cursor

### 5.2 Inputs & Textareas

Form quality directly impacts reporting accuracy. Clear, accessible inputs encourage detailed issue descriptions and reduce submission errors.

**Standard Text Input:**

- **Height:** 48px (comfortable touch target)
- **Background:** White (`#FFFFFF`)
- **Border:** `1px solid #E1E5E9`
- **Border Radius:** 6px
- **Padding:** `0 13px`
- **Font Size:** 15px
- **Text Color:** `#333333`
- **Placeholder:**
  - Color: `#9EA3A9` (muted grey)
  - Font size: 14px
  - Example: "e.g., Corner of Main St and 5th Ave"
- **Focus State:**
  - Border color: `#1A83C5` (primary blue)
  - No outline (use `outline: none`)
  - Transition: `border-color 0.2s ease`
- **Error State:**
  - Border color: `#E03E3E` (red)
  - Error message appears below input
- **Disabled State:**
  - Background: `#F7F8FA`
  - Reduced opacity (0.6)
  - Cursor: `not-allowed`

**Textarea:**

- All standard input styles apply
- Minimum height: 120-150px for issue descriptions
- Vertical resize enabled (`resize: vertical`)
- Generous line-height (1.6) for readability
- Character counter for fields with limits

**Labels:**

- **Font size:** 14px
- **Font weight:** 500 (medium)
- **Color:** `#404040`
- **Margin bottom:** 7px
- **Display:** block
- Always include labels (never rely solely on placeholders)
- Use sentence case, not title case
- Add "(Optional)" suffix for non-required fields

**Helper Text:**

- Font size: 13px
- Color: `#7A7A7A` (muted)
- Appears below input when needed
- Example: "Be as specific as possible to help responders locate the issue"

**Field Validation:**

- Validate on blur, not on every keystroke (reduces frustration)
- Show success states sparingly (green border only for critical fields)
- Error messages should be specific and actionable
- Group related errors together
- Use inline validation for immediate feedback (e.g., password strength)

**Form Layout Guidelines:**

- Stack labels above inputs (better for mobile, translation, and scanning)
- Group related fields visually (e.g., location fields together)
- Place optional fields at the end when possible
- Include field descriptions for complex inputs (e.g., "What3Words location")
- Add character/word counts for limited fields

Labels should sit above fields with small vertical separation.

### 5.3 Tags, Categories & Status Indicators

Tags help users quickly identify issue types, locations, and current status—critical for scanning through multiple reports.

**Category Tags** (Issue types):

- Background: `#26B463` (success green) or category-specific colors
- Text: White (`#FFFFFF`)
- Font size: 13px
- Font weight: 500 (medium)
- Padding: `4px 12px`
- Border radius: 999px (full pill)
- **Examples:** "Street Light", "Road Damage", "Playground", "Graffiti"
- Use consistent colors per category for visual learning

**Status Pills** (Issue state):

- **Open/Pending:** `#1A83C5` (primary blue)
- **In Progress:** `#F59E0B` (orange/amber)
- **Resolved:** `#21A654` (success green)
- **Closed/Rejected:** `#9AA2AF` (muted grey)
- Font size: 13px
- Font weight: 600 (semi-bold)
- Padding: `4px 14px`
- Border radius: 999px
- Text: White (high contrast)

**Location Tags** (Neighborhoods, districts):

- Border: `1px solid #E1E5E9`
- Background: White or light grey
- Text: `#5C6470` (medium grey)
- Font size: 13px
- Font weight: 400 (regular)
- Padding: `4px 12px`
- Border radius: 999px
- **Example:** "Downtown", "East Side", "Zone 3"

**Priority/Urgency Indicators** (optional):

- **High Priority:** Red border/background
- **Medium Priority:** Orange border/background
- **Low Priority:** Grey border/background
- Use sparingly to avoid alarm fatigue

**Tag Guidelines:**

- Maximum 3-4 tags per item to avoid clutter
- Tags should be clickable filters when appropriate
- Maintain consistent order: [Category] [Status] [Location]
- Use tooltips for truncated or abbreviated tag text
- Ensure adequate contrast for accessibility (WCAG AA minimum)

**Badge Counters** (e.g., vote counts, comment counts):

- Background: `#F3F5F8` (light grey)
- Text: `#5C6470` (medium grey)
- Font size: 13px
- Font weight: 600 (semi-bold)
- Padding: `2px 8px`
- Border radius: 12px (soft pill)
- Display inline with icon for context

______________________________________________________________________

## 5A. Issue Cards & List Items

Issue cards are the primary content unit for browsing reports. They must balance information density with scannability.

### 5A.1 Issue Card Structure

**Container:**

- Background: White (`#FFFFFF`)
- Border: `1px solid #E1E5E9`
- Border radius: 12px
- Padding: 20-24px
- Margin bottom: 16px
- Hover: Subtle shadow (`0 2px 8px rgba(0, 0, 0, 0.04)`) and slight background change
- Cursor: pointer (entire card is clickable)

**Card Content Hierarchy:**

1. **Header Row:**

   - Issue title (18px, semi-bold, `#1E2530`)
   - Status pill (right-aligned)

1. **Metadata Line:**

   - Category tag(s)
   - Location (with map pin icon)
   - Timestamp ("2 days ago")
   - Username/Author
   - Separated by dot separators (`·`)
   - Font size: 13px, color: `#7A7A7A`

1. **Description Preview:**

   - First 2-3 lines of issue description
   - 15px, regular weight, `#5C6470`
   - Truncate with ellipsis
   - Line height: 1.6

1. **Footer Row:**

   - Upvote/support counter with icon
   - Comment counter with icon
   - Solution indicator (if applicable)
   - Gap: 16px between items

1. **Image Thumbnail** (if present):

   - Position: Right side or top
   - Border radius: 8px
   - Max height: 120px
   - Object fit: cover

### 5A.2 Compact List Items

For dense views (e.g., map sidebar):

- Reduced padding: 12-16px
- Smaller title: 16px
- Single-line description or no description
- Icon-only counters
- Smaller status indicator

### 5A.3 Empty States

When no issues exist:

- Centered layout
- Illustration or icon (optional)
- Title: 20px, semi-bold
- Description: 15px, muted color
- Call-to-action button
- Generous padding: 48px vertical

______________________________________________________________________

## 6. Navigation & Structural Components

### 6.1 Top Navigation Bar

The global navigation provides consistent wayfinding and access to key features across all pages.

**Structure:**

- **Background:** White (`#FFFFFF`)
- **Border Bottom:** `1px solid #E1E5E9` (subtle separation)
- **Height:** 60-64px (comfortable touch target)
- **Padding:** 16-20px horizontal
- **Z-index:** High value for sticky positioning

**Layout Zones:**

- **Left:** Brand/logo, primary navigation links
- **Center:** Search bar (on browse/map pages)
- **Right:** User profile, notifications, "Create Report" button

**Navigation Links:**

- Font size: 15px
- Font weight: 500 (medium)
- Color: `#5C6470` (inactive), `#1E2530` (active)
- Padding: 8px 20px
- Border radius: 20px (pill shape)
- Hover: Background `#F7F8FA`
- Active state: Background `#21A654` (success green), text white
- Transition: `all 0.2s ease`

**Primary Action Button** ("Create Report"):

- Follows primary button styling
- Always visible for easy access
- Consider fixed/sticky on mobile

**Mobile Navigation:**

- Hamburger menu for narrow viewports
- Off-canvas drawer for navigation links
- Bottom tab bar optional for key actions

### 6.2 Segmented Controls / Tab Navigation

A common pattern for switching between related views or filtering content:

**Container:**

- Background: `#F3F5F8` (light grey)
- Border radius: 7px
- Padding: 2px (creates spacing around tabs)
- Height: 44px
- Display: flex

**Tab Buttons:**

- Flex: 1 (equal width distribution)
- Background: Transparent (inactive), White (active)
- Border: none
- Border radius: 6px
- Font size: 15px
- Font weight: 500 (medium)
- Color: `#7A7A7A` (inactive), `#1C1C1C` (active)
- Padding: `0 34px`
- Cursor: pointer
- Transition: `all 0.2s ease`
- Hover (inactive only): Slightly darker text color

**Use Cases:**

- Filtering issue lists ("All" / "Open" / "Resolved")
- View switching ("Map View" / "List View")
- Content tabs ("Details" / "Comments" / "Solutions")

This creates a clean, iOS-style segmented control for toggling between related content.

### 6.3 Breadcrumbs

For deep navigation hierarchies:

- Font size: 13px
- Color: `#7A7A7A`
- Separator: `/` or `›`
- Current page: `#1E2530` (darker, not clickable)
- Hover: Underline
- Mobile: May collapse to "Back" button

### 6.4 Section Headers

Every major content block begins with a section header styled using the established typographic hierarchy and consistent bottom margin.

- Clear visual separation from content (margin bottom: 16-24px)
- May include action buttons on the right
- Consider sticky headers for long scrolling sections

### 6.5 Pagination & Load More

For long lists of issues:

- **Pagination:** Numbered pages with prev/next
- **Load More:** Button at list end
- **Infinite Scroll:** Auto-load with loading indicator (use cautiously)
- Always indicate current position and total items

______________________________________________________________________

## 7. Modals & Overlays

### 7.1 Overlay Layer

The backdrop uses a semi-opaque dark layer to visually separate the modal from the underlying content but avoid harsh contrast.

- Typical: `rgba(0, 0, 0, 0.35)` to `rgba(0, 0, 0, 0.5)`

### 7.2 Modal Surface

Modals follow the same card principles but typically:

- Have larger padding (e.g., `28px 32px` or similar)
- Are centered within the viewport (use flexbox centering)
- Sit above a darker backdrop
- Use well-defined header, content, and action areas
- Border radius: 12-14px
- Shadow: `0 8px 24px rgba(0, 0, 0, 0.12)` (stronger than cards)

Buttons within modals follow the same global button styling rules.

______________________________________________________________________

## 7A. Responsive Design & Mobile Considerations

Urban issue reporting often happens on-site via mobile devices. Mobile-first design is essential for this platform.

### 7A.1 Breakpoints

**Standard breakpoints:**

- **Mobile:** < 480px (small phones)
- **Mobile Large:** 480px - 768px (large phones, small tablets)
- **Tablet:** 768px - 1024px
- **Desktop:** 1024px - 1440px
- **Wide Desktop:** > 1440px

### 7A.2 Mobile-Specific Patterns

**Touch Targets:**

- Minimum 44x44px for all interactive elements
- Increased spacing between tappable items (minimum 8px)
- Larger buttons on mobile (minimum 48px height)

**Navigation:**

- Hamburger menu or bottom tab bar
- Fixed positioning for primary actions
- Simplified navigation hierarchy

**Forms:**

- Full-width inputs on mobile
- Larger input height (48px minimum)
- Appropriate mobile keyboards (`type="tel"`, `type="email"`, etc.)
- Consider geolocation API for automatic location
- Photo capture directly from camera

**Maps:**

- Larger tap targets for map markers
- Simplified map controls
- Consider collapsible map on mobile list views
- Use device GPS for "Report here" functionality

**Cards:**

- Single column layout
- Reduced padding (16px instead of 24px)
- Simplified metadata (hide non-essential info)
- Stacked action buttons

**Images:**

- Responsive images with `srcset`
- Lazy loading for performance
- Compress user uploads
- Consider lower resolution for slow connections

### 7A.3 Content Priority

**Show on mobile:**

- Issue title and status
- Primary actions
- Essential metadata (location, date)
- Image thumbnails

**Hide or collapse on mobile:**

- Detailed descriptions (show "Read more")
- Extended metadata
- Secondary actions in menu
- Sidebar filters (move to overlay)

### 7A.4 Performance Considerations

- Minimize JavaScript bundle size
- Optimize images aggressively
- Lazy load below-the-fold content
- Consider offline functionality (service workers)
- Show loading states immediately
- Cache static assets

### 7A.5 Progressive Enhancement

- Core functionality works without JavaScript
- Enhanced features for capable devices
- Fallbacks for older browsers
- Graceful degradation of animations

______________________________________________________________________

## 8. Iconography

### 8.1 Style & Selection

Icons communicate function instantly and transcend language barriers—essential for a civic platform serving diverse communities.

**Icon Characteristics:**

- **Style:** Line-based, clean, and minimal (not filled or decorative)
- **Weight:** 1.5-2px stroke width for consistency
- **Size:** 20px or 24px standard (16px for compact contexts)
- **Color:** Inherit from parent text color by default
- **Library:** Use a consistent icon set (e.g., Lucide, Heroicons, Material Icons Outlined)

**Common Icons & Meanings:**

- **Map Pin:** Location/address
- **Alert/Warning Triangle:** Issues requiring attention
- **Check Circle:** Resolved/completed
- **Clock:** Timestamps, pending status
- **Message/Chat:** Comments, discussions
- **Thumbs Up / Arrow Up:** Upvotes, support
- **Camera:** Photo upload
- **Filter:** Filtering options
- **Search:** Search functionality
- **User:** Profile, author
- **Tag:** Categories
- **X / Close:** Dismiss, close modals

**Icon Usage Guidelines:**

- Always pair critical icons with text labels (don't rely on icons alone)
- Use tooltips for icon-only buttons
- Maintain consistent icon style across the application
- Size icons proportionally to adjacent text
- Ensure 3:1 contrast ratio for icons that convey information

### 8.2 Spacing & Alignment

- **Icon-to-text gap:** 6-8px (small) for inline icons
- **Button icons:** 8-10px gap from text
- **Vertical alignment:** Center-align icons with text baseline or center
- Icons should never feel cramped or detached from their context

### 8.3 Interactive Icons

Icons that function as buttons:

- Minimum 44x44px touch target
- Padding around icon for comfortable clicking
- Clear hover state (color change or background)
- Focus state for keyboard navigation
- Consider icon+label for primary actions

### 8.4 Decorative vs. Functional Icons

- **Functional icons** (convey meaning): Must have alt text or labels
- **Decorative icons** (purely visual): Hide from screen readers with `aria-hidden="true"`

______________________________________________________________________

## 9. Interactions & States

### 9.1 Hover States

Interactive elements slightly darken or shift shade to communicate interactivity. Hover effects should remain subtle and consistent.

### 9.2 Focus States

Focus rings or highlighted borders enhance accessibility for navigation via keyboard or assistive tools.

**Standard Focus Pattern:**

- Border color changes to primary blue: `#1A83C5`
- No outline ring (use `outline: none` with border color change)
- Transition: `border-color 0.2s ease`
- Alternative: `box-shadow: 0 0 0 3px rgba(26, 131, 197, 0.15)` for stronger focus indication

### 9.3 Pressed & Active States

Pressed states use deeper versions of the base color, improving tactile feedback.

**Examples:**

- Primary button active: `#125D8F` (darkest blue)
- Tab active: White background with dark text (`#1C1C1C`)

### 9.4 Disabled States

Disabled elements reduce opacity and remove interactive cues. They should never use the same color as active elements.

- Opacity: 0.5-0.6
- Cursor: `not-allowed`
- Remove hover effects

### 9.5 Error States

Form inputs with errors should clearly indicate the problem:

- Border color: `#E03E3E` (red)
- Error message:
  - Color: `#E03E3E`
  - Font size: 13px (0.875rem)
  - Display: block
  - Margin top: 2-4px

______________________________________________________________________

## 10. General Composition Principles

### 10.1 Visual Hierarchy

- Maintain clear hierarchy through spacing, size, and weight—not color or decoration
- Most important actions should be most visually prominent
- Related items grouped closely; unrelated items separated
- Consistent heading levels guide users through content

### 10.2 Color Application

- Use primary blue sparingly—reserve for critical actions only
- Success green indicates positive outcomes and resolved issues
- Maintain high contrast ratios (WCAG AA: 4.5:1 for text, 3:1 for UI components)
- Test designs in grayscale to ensure hierarchy doesn't depend on color alone

### 10.3 Visual Weight & Balance

- Avoid excessive shadows or gradients—maintain clean, modern aesthetic
- Cards should feel light and scannable, not heavy or cluttered
- Balance information density with white space
- Dense data requires more breathing room

### 10.4 Content Prioritization

- Lead with the most important information (issue title, status, location)
- Progressive disclosure: show essentials first, details on demand
- Use truncation and "Read more" for long content
- Reduce visual noise—every element should serve a purpose

### 10.5 Accessibility & Inclusion

- Design for keyboard navigation from the start
- Include visible focus states on all interactive elements
- Provide text alternatives for images and icons
- Test with screen readers
- Support browser zoom up to 200% without breaking layouts
- Use clear, plain language—avoid jargon

### 10.6 Civic Platform Considerations

- **Trust:** Professional, consistent design builds confidence in the platform
- **Transparency:** Clear status indicators show issues are being tracked
- **Empowerment:** Easy reporting and engagement encourage participation
- **Inclusivity:** Accessible design serves the entire community
- **Efficiency:** Respect users' time with streamlined workflows

### 10.7 Performance & Loading

- Prioritize above-the-fold content
- Show loading states for async actions (spinners, skeletons)
- Provide immediate feedback for user actions
- Optimize images (especially user-uploaded photos)
- Progressive enhancement for slower connections

**Core Philosophy:** Every design decision should make it easier for community members to report issues, stay informed, and participate in improving their neighborhoods. The interface should never be a barrier to civic engagement.
