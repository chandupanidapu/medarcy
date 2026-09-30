"""
Medarcy Enterprise Clinical Intelligence Platform

Attachments Domain Entity

Represents supporting clinical resources associated
with a patient case.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import Entity


@dataclass(slots=True)
class Attachments(Entity):
    """
    Supporting clinical resources attached to a patient case.
    """

    documents: List[str] = field(default_factory=list)

    images: List[str] = field(default_factory=list)

    dicom: List[str] = field(default_factory=list)

    ecg: List[str] = field(default_factory=list)

    audio: List[str] = field(default_factory=list)

    video: List[str] = field(default_factory=list)

    other: List[str] = field(default_factory=list)

    def add_document(self, document: str) -> None:
        document = document.strip()
        if document and document not in self.documents:
            self.documents.append(document)

    def add_image(self, image: str) -> None:
        image = image.strip()
        if image and image not in self.images:
            self.images.append(image)

    def add_dicom(self, study: str) -> None:
        study = study.strip()
        if study and study not in self.dicom:
            self.dicom.append(study)

    def add_ecg(self, ecg: str) -> None:
        ecg = ecg.strip()
        if ecg and ecg not in self.ecg:
            self.ecg.append(ecg)

    def add_audio(self, audio: str) -> None:
        audio = audio.strip()
        if audio and audio not in self.audio:
            self.audio.append(audio)

    def add_video(self, video: str) -> None:
        video = video.strip()
        if video and video not in self.video:
            self.video.append(video)

    def add_other(self, resource: str) -> None:
        resource = resource.strip()
        if resource and resource not in self.other:
            self.other.append(resource)

    @property
    def total_resources(self) -> int:
        return (
            len(self.documents)
            + len(self.images)
            + len(self.dicom)
            + len(self.ecg)
            + len(self.audio)
            + len(self.video)
            + len(self.other)
        )