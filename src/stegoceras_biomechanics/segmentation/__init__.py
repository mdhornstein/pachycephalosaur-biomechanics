"""Segmentation module for CT volume thresholding, matrix removal, and label generation.

Phase 4 roadmap:
- DICOM stack loading via SimpleITK / pydicom
- Density thresholding (Hounsfield Unit masking)
- Rock matrix removal and endocranial cavity boundary isolation
- Labelmap export to 3D Slicer / NRRD / NIfTI
"""
