# PEP Documentation
**Title**: svg2png

**Author**: Loghin Catalin 

**Created**: 23-12-2024 

---

## Abstract

This document proposes an implementation of an application that converts an SVG (Scalable Vector Graphics) file into a PNG (Portable Network Graphics) file. The application parses basic SVG elements and renders them into a PNG image without relying on external libraries designed for SVG-to-PNG conversion. Supported elements include: `Rectangle`, `Circle`, `Ellipse`, `Line`, `Path`, and `Polyline`.

---

## Motivation

The purpose of this project is purely educational, to develop a lightweight, custom-built tool for rendering SVG files into PNG format using Python. This implementation focuses on learning the intricacies of SVG rendering and providing a basic, dependency-free solution for simple vector graphics conversion.

---

## Specification

### Functional Overview

1. **Input**:  
   - An SVG file (e.g., `input.svg`) containing basic vector graphic elements.

2. **Output**:  
   - A PNG file (e.g., `output.png`) rendered from the provided SVG.

3. **Limitations**:  
   - Only a subset of SVG elements is supported: `Rectangle`, `Circle`, `Ellipse`, `Line`, `Path`, `Polyline`.
   - Advanced SVG features like gradients, patterns, filters, and animations are not supported.

4. **Error Handling**:  
   - Invalid SVG files result in appropriate error messages.
   - Missing attributes in SVG elements default to reasonable values (e.g., black fill, 1px stroke).

---

### Application Workflow

1. **Command**:  
   ```bash
   python main.py input.svg output.png
