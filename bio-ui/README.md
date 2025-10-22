# Bio Context Enrichment UI

A simple Vue 3 application that demonstrates a biological context enrichment pipeline with a three-step process visualization.

## Features

- **Interactive Query Input**: Enter biological queries and click "Play" to see the enrichment process
- **Visual Pipeline**: Shows the three-step process:
  1. Query Understanding (Classification + Entity Extraction)
  2. Context Enrichment (Tool calls and aggregation)
  3. Reasoning + Rationale (Final ranking with explanations)

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

Then open http://localhost:5173/ (or the port shown in terminal) in your browser.

## Project Structure

- `src/App.vue` - Main single-page component with input and diagram
- `src/main.js` - Vue app initialization
- `vite.config.js` - Vite configuration

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```
