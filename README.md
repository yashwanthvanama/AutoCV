# AutoCV - URL Submission Form

A React application featuring a simple form with a URL input field and submit functionality.

## Features

- Clean, modern UI built with React 18
- URL input field with validation
- Form submission handling
- Responsive design

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **JavaScript** - Programming language

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

Dependencies are already installed. If needed, run:

```bash
npm install
```

### Running the Development Server

Start the development server:

```bash
npm run dev
```

The application will be available at [http://localhost:5173](http://localhost:5173)

### Building for Production

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
AutoCV/
├── src/
│   ├── App.jsx          # Main application component with URL form
│   ├── App.css          # Application styles
│   ├── main.jsx         # Application entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── index.html           # HTML template
└── package.json         # Project dependencies
```

## Usage

1. Enter a valid URL in the input field (e.g., https://example.com)
2. Click the "Submit" button
3. The URL will be logged to the console and displayed in an alert

You can customize the `handleSubmit` function in `src/App.jsx` to add your own URL processing logic.

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## License

MIT

