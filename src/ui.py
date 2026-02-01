import glob
import os
import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QComboBox, QProgressBar, QMessageBox, QFileDialog, QCheckBox, QHBoxLayout
)
from PySide6.QtCore import Qt, QThread, Signal, QStandardPaths

from extractor import extract_youtube_stream
from downloader import download_youtube
from utils import is_youtube_link


class DownloadThread(QThread):
    progress_signal = Signal(float, int, int)
    finished_signal = Signal()
    paused_signal = Signal()
    cancelled_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, url, resolution, folder, audio_only, video_only):
        super().__init__()
        self.url = url
        self.resolution = resolution
        self.folder = folder
        self.audio_only = audio_only
        self.video_only = video_only
        self.control_flag = {
            "pause": False,
            "cancel": False
        }

    def run(self):
        try:
            download_youtube(
                self.url,
                self.resolution,
                self.progress_signal.emit,
                self.control_flag,
                self.folder,
                self.audio_only,
                self.video_only
            )
            self.finished_signal.emit()

        except Exception as e:
            msg = str(e).lower()

            if "paused" in msg:
                self.paused_signal.emit()
            elif "cancelled" in msg:
                self.cancelled_signal.emit()
            else:
                self.error_signal.emit(str(e))

    def pause(self):
        self.control_flag["pause"] = True

    def cancel(self):
        self.control_flag["cancel"] = True


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        def resource_path(relative_path):
            if hasattr(sys, "_MEIPASS"):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.join(os.path.abspath("."), relative_path)

        self.setWindowIcon(QIcon(resource_path("icon.ico")))

        self.quality_size_map = {}
        self.setWindowTitle("DownTube")
        self.resize(450, 250)
        self.setFixedSize(600, 450)

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - 450) // 2
        y = (screen.height() - 250) // 2
        self.move(x, y)

        self.download_folder = QStandardPaths.writableLocation(
                                                QStandardPaths.DownloadLocation
                                                )

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        layout.addWidget(self.url_input)

        self.fetch_btn = QPushButton("Fetch Qualities")
        self.fetch_btn.clicked.connect(self.fetch_qualities)
        layout.addWidget(self.fetch_btn)

        self.title_label = QLabel("Title: -")
        layout.addWidget(self.title_label)

        self.quality_box = QComboBox()
        self.quality_box.currentIndexChanged.connect(self.update_size)
        layout.addWidget(self.quality_box)

        mode_layout = QHBoxLayout()

        self.audio_only_cb = QCheckBox("Audio only (MP3)")
        self.video_only_cb = QCheckBox("Video only (No audio)")

        mode_layout.addWidget(self.audio_only_cb)
        mode_layout.addWidget(self.video_only_cb)

        layout.addLayout(mode_layout)

        self.audio_only_cb.stateChanged.connect(self.on_mode_changed)
        self.video_only_cb.stateChanged.connect(self.on_mode_changed)
        # self.video_only_cb.hide()

        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        self.folder_label = QLabel(f"Save to: {self.download_folder}")
        layout.addWidget(self.folder_label)

        self.folder_btn = QPushButton("Choose Download Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        layout.addWidget(self.folder_btn)

        self.size_label = QLabel("Estimated Size: -")
        layout.addWidget(self.size_label)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_download)
        self.pause_btn.setEnabled(False)
        layout.addWidget(self.pause_btn)

        self.resume_btn = QPushButton("Resume")
        self.resume_btn.clicked.connect(self.resume_download)
        self.resume_btn.setEnabled(False)
        layout.addWidget(self.resume_btn)


        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.progress_label = QLabel("0%")
        layout.addWidget(self.progress_label)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_download)
        self.cancel_btn.setEnabled(False)
        layout.addWidget(self.cancel_btn)

        self.setLayout(layout)

        self.setStyleSheet("""
                    QWidget {
                        background-color: #334155;
                        color: #e5e7eb;
                        font-size: 14px;
                    }
                    
                    QLineEdit {
                        background-color: #020617;
                        border: 1px solid #fff;
                        border-radius: 6px;
                        padding: 6px;
                    }
                    
                    QPushButton {
                        background-color: #296d98;
                        color: #fff;
                        border-radius: 6px;
                        padding: 8px;
                        font-weight: bold;
                    }
                    
                    QPushButton:hover {
                        background-color: #3792cb;
                    }
                    
                    QPushButton:disabled {
                        background-color: #1c4966;
                        color: #94a3b8;
                    }
                    
                    QComboBox {
                        background-color: #1c4966;
                        border: 1px solid #fff;
                        border-radius: 6px;
                        padding: 6px;
                    }
                    
                    QProgressBar {
                        border: 1px solid #22c55e;
                        border-radius: 6px;
                        text-align: center;
                    }
                    
                    QProgressBar::chunk {
                        background-color: #22c55e;
                    }
                    """)


        self.video_formats = []
        self.audio_formats = []
        self.paused_url = None
        self.paused_resolution = None
        self.is_paused = False

    def fetch_qualities(self):
        url = self.url_input.text().strip()

        if not is_youtube_link(url):
            QMessageBox.critical(self, "Error", "Invalid YouTube URL")
            return

        stream = extract_youtube_stream(url)

        self.title_label.setText("Title: " + stream["title"])
        self.quality_box.clear()
        self.quality_box.addItems([str(q) for q in stream["qualities"]])

        self.video_formats = stream["video_formats"]
        self.audio_formats = stream["audio_formats"]

        self.quality_size_map.clear()

        # pick best audio size once
        audio_size = 0
        if self.audio_formats:
            audio_size = self.audio_formats[0].get("filesize") \
                or self.audio_formats[0].get("filesize_approx", 0)

        for vf in self.video_formats:
            height = vf.get("height")
            video_size = vf.get("filesize") or vf.get("filesize_approx", 0)

            if height and video_size:
                total_size_mb = (video_size + audio_size) / (1024 * 1024)
                self.quality_size_map[height] = round(total_size_mb, 2)


        self.update_size()
    
    def on_mode_changed(self):
        if self.audio_only_cb.isChecked():
            self.video_only_cb.setChecked(False)
            self.quality_box.setEnabled(False)

        elif self.video_only_cb.isChecked():
            self.audio_only_cb.setChecked(False)
            self.quality_box.setEnabled(True)

        else:
            # normal mode (video + audio)
            self.quality_box.setEnabled(True)

    def update_size(self):
        try:
            res = int(self.quality_box.currentText())
        except ValueError:
            self.size_label.setText("Estimated Size: -")
            return

        size = self.quality_size_map.get(res)

        if size:
            self.size_label.setText(f"Estimated Size: {size} MB")
        else:
            self.size_label.setText("Estimated Size: Unknown")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Download Folder",
            self.download_folder
        )

        if folder:
            self.download_folder = folder
            self.folder_label.setText(f"Save to: {folder}")



    def start_download(self):
        url = self.url_input.text().strip()

        if not is_youtube_link(url):
            QMessageBox.critical(self, "Error", "Invalid YouTube URL")
            return

        self.audio_only = self.audio_only_cb.isChecked()
        self.video_only = self.video_only_cb.isChecked()

        resolution = None
        if not self.audio_only:
            resolution = int(self.quality_box.currentText())

        # Reset paused state
        self.is_paused = False
        self.paused_url = None
        self.paused_resolution = None

        self.progress_bar.setValue(0)
        self.progress_label.setText("Starting...")

        self.download_thread = DownloadThread(url, resolution, self.download_folder,self.audio_only,self.video_only)
        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)
        self.download_thread.cancelled_signal.connect(self.download_cancelled)
        self.audio_only_cb.stateChanged.connect(
                                                lambda state: self.quality_box.setEnabled(not state)
                                                )

        self.pause_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)

        self.download_thread.start()

    
    def pause_download(self):
        if not hasattr(self, "download_thread"):
            return
    
        if not self.download_thread.isRunning():
            return
    
        self.paused_url = self.download_thread.url
        self.paused_resolution = self.download_thread.resolution
        self.is_paused = True
    
        self.download_thread.pause()
    
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(True)

    def resume_download(self):
        if not self.is_paused:
            return

        self.download_thread = DownloadThread(
            self.paused_url,
            self.paused_resolution,
            self.download_folder,
            self.audio_only,
            self.video_only
        )

        self.download_thread.progress_signal.connect(self.update_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.paused_signal.connect(self.download_paused)
        self.download_thread.error_signal.connect(self.download_error)

        self.download_thread.start()

        self.pause_btn.setEnabled(True)
        self.resume_btn.setEnabled(False)

    
    def download_paused(self):
        self.progress_label.setText("Paused")

    def cancel_download(self):
        # stop running thread if exists
        if hasattr(self, "download_thread") and self.download_thread.isRunning():
            self.download_thread.cancel()

        # delete .part files from download folder
        part_pattern = os.path.join(self.download_folder, "*.part")
        ytdl_pattern = os.path.join(self.download_folder, "*.ytdl")

        for f in glob.glob(part_pattern) + glob.glob(ytdl_pattern):
            try:
                os.remove(f)
            except Exception:
                pass

        # reset state
        self.is_paused = False
        self.paused_url = None
        self.paused_resolution = None

        self.progress_bar.setValue(0)
        self.progress_label.setText("Cancelled")

        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

        QMessageBox.information(
            self,
            "Cancelled",
            "Download cancelled and temporary files removed."
        )




    def download_cancelled(self):
        self.is_paused = False
        self.paused_url = None
        self.paused_resolution = None

        self.progress_bar.setValue(0)
        self.progress_label.setText("Cancelled")

        self.download_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)




    def update_progress(self, percent, downloaded, total):
        self.progress_bar.setValue(int(percent))
        self.progress_label.setText(f"{percent:.1f}%")

    def download_finished(self):
        self.pause_btn.setEnabled(False)
        self.resume_btn.setEnabled(False)
        QMessageBox.information(self, "Done", "Download completed successfully!")

    def download_error(self, msg):
        QMessageBox.critical(self, "Error", msg)

