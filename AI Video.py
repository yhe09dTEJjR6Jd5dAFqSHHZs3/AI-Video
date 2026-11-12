import concurrent.futures
import difflib
import tempfile
import ctypes
import datetime
import gc
import hashlib
import html
import importlib
import importlib.metadata
import json
import locale
import math
import array
import secrets
import os
import platform
import queue
import random
import re
import shutil
import struct
import subprocess
import sys
import threading
import time
import traceback
import urllib.error
import urllib.parse
import urllib.request
import wave
import weakref
import zipfile
from collections import deque
from pathlib import Path, PurePosixPath

APP_NAME = "离线 AI 视频工坊"
APP_VERSION = "2.4.0"
RUNTIME_VERSION = "2026.11.12.6"
PIPELINE_VERSION = "2026.11.12.6"
MIN_PYTHON = (3, 10)
MAX_PYTHON = (3, 13)
GB = 1024 ** 3
DEFAULT_FPS = 24
SPEECH_RATE = 16000
ASR_WINDOW_SECONDS = 30
MAX_ASR_USER_WINDOWS = 36
MAX_ASR_INPUTS = 16
MIN_SPEECH_SIMILARITY = .37
MIN_SPEECH_REVIEW_CHARS = 12
MAX_NATIVE_SEGMENTS = 12
MAX_NEIGHBOR_FRAME_DIFFERENCE = 98
OCR_PAGES = 96
OCR_PAGE_SCALE = 1.5
SOURCE_METADATA_TIMEOUT = 15
EXTERNAL_COMMAND_HISTORY = 160
EXTERNAL_COMMAND_LOCK = threading.Lock()
EXTERNAL_COMMAND_EVENTS = deque(maxlen=EXTERNAL_COMMAND_HISTORY)
MIN_INSTALL_FREE = 8 * GB
MIN_JOB_FREE = 2 * GB
MAX_SCENE_ATTEMPTS = 3
MAX_REPAIR_PASSES = 2
MAX_TEMPORAL_RETRIES = 2
MIN_CLIP_ABSOLUTE_COSINE = 0.12
MIN_CLIP_ABSOLUTE_MARGIN = 0.008
NATIVE_SMOKE_FRAMES = 17
NATIVE_SMOKE_STEPS = 1
NATIVE_SMOKE_TIMEOUT = 1800
REVIEW_PASS = "passed"
REVIEW_FAIL = "failed"
REVIEW_UNAVAILABLE = "unavailable"
REVIEW_NOT_APPLICABLE = "not_applicable"
MAX_SPEECH_SPEEDUP = 1.30
SPEECH_END_MARGIN = 0.12
STOP_GRACE_SECONDS = 18
MAX_FINAL_DURATION_DRIFT = 0.008
MIN_CLIP_COSINE = 0.16
MIN_CLIP_MARGIN = 0.015
PROGRESS_PREFIX = "OFFLINE_STUDIO_EVENT:"
MAX_DOCUMENT_BYTES = 24 * 1024 * 1024
MAX_DOCUMENT_XML_BYTES = 8 * 1024 * 1024
MAX_DOCUMENT_TEXT = 256000
MAX_FINGERPRINT_FULL_BYTES = 16 * 1024 * 1024
FINGERPRINT_SAMPLE_BYTES = 1024 * 1024
MODEL_SWITCH_FREE_BYTES = 5 * GB
FFMPEG_INPUT_TIMEOUT = 180
FIRST_LAST_HOLD_SECONDS = 0.35
BOUNDARY_FRAME_MEAN_DIFF_MAX = 24
VOICE_REPO = "rhasspy/piper-voices"
VOICE_REVISION = "217ddc79818708b078d0d14a8fae9608b9d77141"
VOICE_FILE = "zh/zh_CN/huayan/medium/zh_CN-huayan-medium.onnx"
VOICE_SHA256 = "9929917bf8cabb26fd528ea44d3a6699c11e87317a14765312420be230be0f3d"
VOICE_PACKAGES = ("piper-tts==1.8.0",)
MODEL_CHECK_MIN_BYTES = 1024 * 1024
MODEL_HASH_SAMPLE_BYTES = 64 * 1024
TORCH_VERSION = "2.7.1"
CUDA_MIN_TOTAL_MB = 4096
CUDA_MIN_FREE_BYTES = 3 * GB
EXTERNAL_OUTPUT_QUEUE = 2048
EXTERNAL_ERROR_LINES = 18
UI_RECOMMEND_DELAY_MS = 450
UI_MAX_ASSET_ROWS = 5
UI_MAX_SCENE_ROWS = 6
UI_PREVIEW_IMAGE_LIMIT = 520
ASSET_MATCH_FACTOR = 4
ASSET_MATCH_LIMIT = 24
MAX_MODEL_DOWNLOAD_WORKERS = 4
MAX_DOWNLOAD_PROCESSES = 2
MIN_PARALLEL_DOWNLOAD_FREE = 20 * GB
MIN_FINAL_SEMANTIC_RETENTION = .78
MIN_SYSTEM_MEMORY_HEADROOM = 2 * GB
SYSTEM_MEMORY_RESERVE_FRACTION = .18
MIN_GPU_HEADROOM = 1024 * 1024 * 1024
MIN_WORKSPACE_PATH_MARGIN = 118
MAX_REFERENCE_BUDGET = 6400
MAX_DIRECTOR_CONTEXT = 4096
MAX_SPEECH_RESPONSE_SECONDS = 150
RESOURCE_METRICS_LIMIT = 96
MAX_IMAGE_PIXELS = 1024 * 1024
MIN_IMAGE_DIMENSION = 192
NATIVE_VIDEO_MIN_FREE_MB = 16 * 1024
MIN_DISK_DOWNLOAD_RESERVE = MIN_JOB_FREE
VIDEO_MODEL_FOLDER = "video"
OPTIONAL_MODEL_FOLDERS = {"director": "director_plus", "painter": "painter_plus",
                          "listener": "listener_plus", "inspector": "inspector_plus"}
NATIVE_VIDEO_FPS = 8
NATIVE_VIDEO_FRAMES = 49
NATIVE_VIDEO_MAX_FRAMES = 81
MAX_NATIVE_ATTEMPTS = 2
MAX_NATIVE_OUTPUT_DURATION_FACTOR = 1.04
NATIVE_VIDEO_MAX_SLOWDOWN = 1.5
NATIVE_REVIEW_FRACTIONS = (.02, .17, .34, .50, .66, .83, .98)
MODEL_INTEGRITY_EXTENSIONS = {".bin", ".safetensors", ".json", ".model", ".txt", ".py", ".onnx"}
RESOURCE_MONITOR_INTERVAL = 5
DOWNLOAD_SPACE_MULTIPLIER = 1.4
MODEL_SIZE_ESTIMATES = {"director": 2 * GB, "painter": 3 * GB, "listener": GB, "inspector": GB, "voice": GB // 2}
MIN_CAPTION_FONT = 13
MAX_CAPTION_LINES = 3
CAPTION_MAX_WIDTH_FRACTION = .86
CAPTION_SEGMENT_GAP_FRAMES = 1
MAX_CAPTION_SEGMENTS = 12
MIN_NATIVE_TEMPORAL_DIFFERENCE = .7
MAX_NATIVE_TEMPORAL_DIFFERENCE = 80.0
MIN_MOTION_REVIEW_FRAMES = 3
MAX_ASR_CACHE_ENTRIES = 120
NATIVE_VIDEO_STEPS = {"快速": 12, "智能": 18, "精细": 25}
MIN_DIRECTOR_USABLE_RAM = GB // 2
MIN_PAINTER_USABLE_RAM = GB
MIN_INSPECTOR_USABLE_RAM = GB // 2
CLIP_DURATION_TOLERANCE = .18
AMBIENT_VOLUME = .32
NATIVE_COMPONENTS = ("transformer", "vae", "text_encoder", "tokenizer", "scheduler")
NATIVE_RESOLUTIONS = {
    "横屏": ((768, 432), (512, 288), (384, 216), (256, 144)),
    "竖屏": ((432, 768), (288, 512), (216, 384), (144, 256)),
    "方形": ((576, 576), (448, 448), (384, 384), (320, 320), (256, 256))}
NATIVE_HIGH_MEMORY = 24 * GB
NATIVE_SEAM_DIFFERENCE_MAX = 58.0
NATIVE_MAX_SEAM_SAMPLES = 16
VOICE_PROBE_SECONDS = 60
VOICE_PROBE_LOCK = threading.RLock()
VOICE_PROBE_CACHE = {}
MIN_MIXED_VOICE_RMS = .0015
MIN_MIXED_VOICE_CORRELATION = .15
MAX_VOICE_CORRELATION_SECONDS = 9
MAX_VOICE_ALIGNMENT_SECONDS = .32
TORCH_WHEEL_INDEX = "https://download.pytorch.org/whl"
MODEL_SPECS = (
    ("分镜与文案", "Qwen/Qwen2.5-0.5B-Instruct", "director", ("*.json", "*.txt", "*.model", "*.safetensors")),
    ("画面生成", "segmind/tiny-sd", "painter", ("*.json", "*.txt", "*.model", "*.bin")),
    ("语音识别", "openai/whisper-tiny", "listener", ("*.json", "*.txt", "*.model", "*.safetensors")),
    ("画面语义审校", "openai/clip-vit-base-patch32", "inspector", ("*.json", "*.txt", "*.model", "*.bin")),
)
MODEL_REVISIONS = {
    "Qwen/Qwen2.5-0.5B-Instruct": "7ae557604adf67be50417f59c2c2f167def9a775",
    "segmind/tiny-sd": "cad0bd7495fa6c4bcca01b19a723dc91627fe84f",
    "openai/whisper-tiny": "169d4a4341b33bc18d8881c4b69c2e104e1cc0af",
    "openai/clip-vit-base-patch32": "3d74acf9a28c67741b2f4f2ea7635f0aaf6f0268",
}
TRUSTED_MODEL_WEIGHTS = {
    "Qwen/Qwen2.5-0.5B-Instruct": {
        "model.safetensors": "fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe"},
    "segmind/tiny-sd": {
        "unet/diffusion_pytorch_model.bin": "c9b63e57cb1479c946c73bf5484bc1a823dbe565158ea0ee40015a18844d9f29",
        "text_encoder/pytorch_model.bin": "f99d8915149c782551f7d14aae5ca0b6e76a6e94d30e5dc86a349b228fbf92ad",
        "vae/diffusion_pytorch_model.bin": "279228e5296858f5d330db506ff6a51fdcad0d69f87634b5e9133406110af9bf"},
    "openai/whisper-tiny": {
        "model.safetensors": "7ebd0e69e78190ffe1438491fa05cc1f5c1aa3a4c4db3bc1723adbb551ea2395"},
    "openai/clip-vit-base-patch32": {
        "pytorch_model.bin": "a63082132ba4f97a80bea76823f544493bffa8082296d62d71581a4feff1576f"},
}
MIN_DISK_CACHE_RESERVE = GB
RUNTIME_BACKUP_FOLDER = "venv.rollback"
SOURCE_COPY_CHUNK = 2 * 1024 * 1024
BATTERY_RESOURCE_FRACTION = .8
MAX_ASSETS_PER_SCENE = 12
MIN_ASSET_SHOT_SECONDS = .45


NATIVE_AUTO_REPO = "zai-org/CogVideoX-2b"
NATIVE_AUTO_MIN_TOTAL_MB = 20 * 1024
NATIVE_AUTO_MIN_RAM = 16 * GB
NATIVE_AUTO_RETRY_SECONDS = 24 * 3600
NATIVE_AUTO_DISK_RESERVE = 8 * GB
MODEL_DOWNLOAD_SECURITY_SUFFIXES = {".safetensors", ".json", ".model", ".txt"}
RESOURCE_PRESSURE_STREAK = 2
RESOURCE_MONITOR_CPU_LIMIT = 0.86
RESOURCE_MAX_CPU_SHARE = 0.65
DOCUMENT_REQUIRED_PATTERN = re.compile(r"必须|严格按照|严格依据|仅根据|完全根据|务必引用|以.*(?:文档|材料|附件|资料).*为准|根据.*(?:文档|资料|附件)")

CORE_PACKAGE_SPECS = (
    "pillow>=10,<13", "numpy>=1.26,<2.3", "transformers==4.49.0", "sentencepiece>=0.2,<1",
    "accelerate>=1.4,<2", "safetensors>=0.4,<1",
    "huggingface-hub>=0.30,<1", "imageio-ffmpeg>=0.5,<1",
)
EXTENDED_PACKAGE_SPECS = ("diffusers==0.33.1", "pypdf>=5,<9")
OPTIONAL_OCR_PACKAGE_SPECS = ("pypdfium2>=4.30,<6", "rapidocr>=3.10,<5", "onnxruntime>=1.20,<2")
OPTIONAL_OCR_PACKAGE_IMPORTS = {"pypdfium2": "pypdfium2", "rapidocr": "rapidocr", "onnxruntime": "onnxruntime"}
CORE_PACKAGE_IMPORTS = {
    "torch": "torch", "transformers": "transformers", "accelerate": "accelerate",
    "safetensors": "safetensors", "huggingface-hub": "huggingface_hub",
    "imageio-ffmpeg": "imageio_ffmpeg", "pillow": "PIL", "numpy": "numpy",
    "sentencepiece": "sentencepiece",
}
EXTENDED_PACKAGE_IMPORTS = {"diffusers": "diffusers", "pypdf": "pypdf"}
VIDEO_TYPES = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
AUDIO_TYPES = {".wav", ".mp3", ".flac", ".m4a", ".aac", ".ogg", ".wma"}
IMAGE_TYPES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}
DOC_TYPES = {".txt", ".md", ".csv", ".json", ".pdf", ".docx", ".html", ".htm", ".srt"}
RUNNING_CHILDREN = weakref.WeakSet()
RUNNING_CHILDREN_LOCK = threading.Lock()


def now_stamp():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def slug(value, length=34):
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", str(value))
    value = re.sub(r"\s+", "_", value).strip(" ._")
    return value[:length] or "作品"


def request_fingerprint(request):
    payload = json.loads(json.dumps(request, ensure_ascii=False, default=str))
    for group, paths in payload.get("files", {}).items():
        payload["files"][group] = []
        for name in paths:
            path = Path(name)
            try:
                info = path.stat()
                digest = hashlib.sha256()
                with path.open("rb") as stream:
                    if info.st_size <= MAX_FINGERPRINT_FULL_BYTES:
                        for chunk in iter(lambda: stream.read(FINGERPRINT_SAMPLE_BYTES), b""):
                            digest.update(chunk)
                    else:
                        for offset in (0, max(0, (info.st_size - FINGERPRINT_SAMPLE_BYTES) // 2),
                                       max(0, info.st_size - FINGERPRINT_SAMPLE_BYTES)):
                            stream.seek(offset)
                            digest.update(stream.read(FINGERPRINT_SAMPLE_BYTES))
                payload["files"][group].append((str(path.resolve()), info.st_size,
                                                info.st_mtime_ns, digest.hexdigest()))
            except OSError:
                payload["files"][group].append((str(path), None, None))
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + "." + secrets.token_hex(8) + ".partial")
    try:
        tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def read_json(path, default=None):
    try:
        parsed = json.loads(Path(path).read_text(encoding="utf-8"))
        return parsed if default is None or isinstance(parsed, type(default)) else default
    except (OSError, ValueError, TypeError):
        return default


def memory_info():
    if os.name != "nt":
        try:
            page = os.sysconf("SC_PAGE_SIZE")
            allmem = os.sysconf("SC_PHYS_PAGES") * page
            freemem = os.sysconf("SC_AVPHYS_PAGES") * page
            return {"total": allmem, "available": freemem}
        except (OSError, ValueError, AttributeError):
            return {"total": 0, "available": 0}
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    state = MEMORYSTATUSEX()
    state.dwLength = ctypes.sizeof(state)
    if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(state)):
        return {"total": state.ullTotalPhys, "available": state.ullAvailPhys}
    return {"total": 0, "available": 0}


def gpu_info():
    result = {"name": "", "free_mb": 0, "total_mb": 0, "driver": "", "index": None, "devices": []}
    try:
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        proc = subprocess.run(["nvidia-smi", "--query-gpu=index,name,memory.free,memory.total,driver_version,uuid",
                               "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=6,
                              creationflags=flags)
        devices = []
        if proc.returncode == 0:
            for line in proc.stdout.splitlines():
                fields = [field.strip() for field in line.split(",")]
                if len(fields) < 6:
                    continue
                try:
                    devices.append({"physical_index": int(fields[0]), "index": int(fields[0]),
                                    "name": fields[1], "free_mb": int(fields[2]),
                                    "total_mb": int(fields[3]), "driver": fields[4], "uuid": fields[5]})
                except (ValueError, IndexError):
                    continue
        visible = os.environ.get("CUDA_VISIBLE_DEVICES")
        if visible is not None:
            ordered = []
            for token in (part.strip() for part in visible.split(",")):
                if not token or token == "-1":
                    continue
                found = next((item for item in devices if token == str(item["physical_index"]) or
                              token == item["uuid"] or item["uuid"].startswith(token)), None)
                if found is not None and found not in ordered:
                    ordered.append(found)
            devices = [{**item, "index": index} for index, item in enumerate(ordered)]
        if devices:
            preferred = max(devices, key=lambda item: (item["free_mb"], item["total_mb"]))
            result.update(preferred)
            result["devices"] = devices
    except (ValueError, OSError, subprocess.TimeoutExpired):
        pass
    return result


def torch_cuda_devices(torch):
    devices = []
    try:
        if not torch.cuda.is_available():
            return devices
        for index in range(torch.cuda.device_count()):
            try:
                free, total = torch.cuda.mem_get_info(index)
                props = torch.cuda.get_device_properties(index)
                devices.append({"index": index, "name": props.name,
                                "free_mb": int(free // (1024 * 1024)),
                                "total_mb": int(total // (1024 * 1024)),
                                "free_bytes": int(free), "total_bytes": int(total)})
            except (RuntimeError, AssertionError, ValueError):
                continue
    except (RuntimeError, AssertionError, ValueError):
        pass
    return devices


def select_torch_gpu(torch, minimum_free=0, preferred=None):
    candidates = [item for item in torch_cuda_devices(torch) if item["free_bytes"] >= minimum_free]
    if preferred:
        candidates = [item for item in candidates if item["name"] == preferred.get("name") and
                      (preferred.get("index") is None or item["index"] == preferred["index"]) and
                      abs(item["total_mb"] - (preferred.get("total_mb") or 0)) <=
                      max(256, int((preferred.get("total_mb") or 0) * .04))]
    return max(candidates, key=lambda item: (item["free_bytes"], item["total_bytes"])) if candidates else None

class ResourceGovernor:
    def __init__(self, root=None):
        self.root = Path(root) if root else None
        self.peak_ram_pressure = 0.0
        self.lowest_available_ram = None
        self.lowest_available_gpu = None
        self.samples = []
        self._gpu_snapshot = {}
        self._gpu_checked = 0.0
        self._cuda_torch = None
        self._cuda_index = None
        self._monitor_stop = threading.Event()
        self._monitor_thread = None
        self.resource_stop_reason = None
        self._lock = threading.RLock()
        self.pressure_events = []
        self._cpu_previous = None
        self._cpu_busy = None
        self._power = system_power_state()
        self._power_checked = 0.0

    def attach_cuda(self, torch_module=None, index=None):
        with self._lock:
            self._cuda_torch = torch_module if index is not None else None
            self._cuda_index = index
            self._gpu_checked = 0.0

    def start_monitor(self, cancel=None, notify=None):
        if self._monitor_thread is not None and self._monitor_thread.is_alive():
            return
        self._monitor_stop.clear()
        def monitor():
            streak = 0
            while not self._monitor_stop.wait(RESOURCE_MONITOR_INTERVAL):
                try:
                    sample = self.snapshot("live_resource_check")
                    total = sample["ram_total"]
                    danger_ram = total and sample["ram_available"] < max(512 * 1024 * 1024, int(total * .05))
                    free_disk = sample["disk_free"]
                    danger_disk = free_disk is not None and free_disk < MIN_JOB_FREE // 4
                    streak = streak + 1 if danger_ram or danger_disk else 0
                    if streak >= RESOURCE_PRESSURE_STREAK:
                        self.resource_stop_reason = ("可用内存持续低于安全阈值" if danger_ram else
                                                     "工作磁盘空间已接近耗尽")
                        if notify:
                            notify("为保护设备已请求停止：" + self.resource_stop_reason)
                        if isinstance(cancel, StopSignal):
                            cancel.filename.touch()
                        elif isinstance(cancel, threading.Event):
                            cancel.set()
                        break
                except (OSError, ValueError) as error:
                    if notify:
                        notify("资源采样跳过一次：" + type(error).__name__)
        self._monitor_thread = threading.Thread(target=monitor, daemon=True)
        self._monitor_thread.start()

    def stop_monitor(self):
        self._monitor_stop.set()
        if self._monitor_thread and threading.current_thread() is not self._monitor_thread:
            self._monitor_thread.join(timeout=1.0)
        self._monitor_thread = None

    def snapshot(self, stage=""):
        with self._lock:
            ram = memory_info()
            moment = time.monotonic()
            if moment - self._gpu_checked >= RESOURCE_MONITOR_INTERVAL or not self._gpu_snapshot:
                self._gpu_snapshot = gpu_info()
                self._gpu_checked = moment
            gpu = dict(self._gpu_snapshot)
            if self._cuda_torch is not None and self._cuda_index is not None:
                try:
                    free_bytes, total_bytes = self._cuda_torch.cuda.mem_get_info(self._cuda_index)
                    device_name = self._cuda_torch.cuda.get_device_properties(self._cuda_index).name
                    gpu.update({"free_mb": free_bytes // (1024 * 1024),
                                "total_mb": total_bytes // (1024 * 1024),
                                "index": self._cuda_index, "name": device_name,
                                "devices": [{"index": self._cuda_index, "name": device_name}]})
                except (RuntimeError, AssertionError, ValueError):
                    gpu.update({"free_mb": 0, "index": self._cuda_index, "devices": []})
            current_cpu = cpu_time_sample()
            if current_cpu and self._cpu_previous:
                idle_diff = current_cpu[0] - self._cpu_previous[0]
                total_diff = current_cpu[1] - self._cpu_previous[1]
                if total_diff > 0:
                    self._cpu_busy = round(max(0.0, min(1.0, 1.0 - idle_diff / total_diff)), 3)
            self._cpu_previous = current_cpu
            if moment - self._power_checked >= RESOURCE_MONITOR_INTERVAL:
                self._power = system_power_state()
                self._power_checked = moment
            free = int(ram.get("available", 0))
            total = int(ram.get("total", 0))
            gpu_free = max(0, int(gpu.get("free_mb", 0))) * 1024 * 1024
            reserve = max(MIN_SYSTEM_MEMORY_HEADROOM, int(total * SYSTEM_MEMORY_RESERVE_FRACTION))
            usable = max(0, free - reserve)
            if total:
                self.peak_ram_pressure = max(self.peak_ram_pressure, 1 - free / total)
            self.lowest_available_ram = (free if self.lowest_available_ram is None
                                         else min(free, self.lowest_available_ram))
            if gpu.get("devices"):
                self.lowest_available_gpu = (gpu_free if self.lowest_available_gpu is None
                                             else min(gpu_free, self.lowest_available_gpu))
            sample = {"stage": str(stage)[:80], "ram_available": free, "ram_usable": usable,
                      "ram_total": total, "gpu_free": gpu_free, "gpu_index": gpu.get("index"),
                      "disk_free": shutil.disk_usage(self.root).free if self.root and self.root.exists() else None,
                      "cpu_busy": self._cpu_busy,
                      "on_battery": self._power.get("on_battery", False),
                      "battery_percent": self._power.get("percent"),
                      "at": datetime.datetime.now().isoformat()}
            self.samples.append(sample)
            if len(self.samples) > RESOURCE_METRICS_LIMIT:
                del self.samples[:-RESOURCE_METRICS_LIMIT]
            return dict(sample)

    def budget(self, stage, ram_bytes=0, gpu_bytes=0, disk_bytes=0, device="cpu"):
        sample = self.snapshot(stage)
        if sample["ram_total"] and sample["ram_usable"] < int(ram_bytes):
            raise RuntimeError("本机可用内存不足以安全执行 %s" % stage)
        if device == "cuda" and sample["gpu_free"] < int(gpu_bytes) + MIN_GPU_HEADROOM:
            raise RuntimeError("当前空闲显存不足以安全执行 %s" % stage)
        if sample["disk_free"] is not None and sample["disk_free"] < MIN_JOB_FREE + int(disk_bytes):
            raise RuntimeError("工作目录剩余空间不足以安全执行 %s" % stage)
        return sample

    def adaptive_pause(self, stage, cancel=None, notify=None, allowance=4):
        for number in range(allowance + 1):
            if cancel is not None and cancel.is_set():
                raise InterruptedError("已停止")
            sample = self.snapshot(stage)
            total = sample["ram_total"]
            pressure = bool(total and sample["ram_available"] < max(
                MIN_SYSTEM_MEMORY_HEADROOM, int(total * SYSTEM_MEMORY_RESERVE_FRACTION)))
            busy_cpu = sample.get("cpu_busy") is not None and sample["cpu_busy"] > RESOURCE_MONITOR_CPU_LIMIT
            on_battery = sample.get("on_battery")
            if not pressure:
                if busy_cpu and number == 0:
                    if notify:
                        notify("检测到其他任务较忙，降低本进程负载后继续")
                    time.sleep(.85 if on_battery else .4)
                elif on_battery:
                    time.sleep(.2)
                return sample
            with self._lock:
                self.pressure_events.append({"stage": stage, "at": sample["at"],
                                             "ram_available": sample["ram_available"]})
                self.pressure_events = self.pressure_events[-RESOURCE_METRICS_LIMIT:]
            if number == allowance:
                raise RuntimeError("其他软件占用较多内存，已保护设备并停止当前阶段：" + stage)
            if notify:
                notify("检测到其他程序占用大量内存，短暂等待并降低创作负载")
            gc.collect()
            time.sleep(min(2, .5 + number * .35))

    def image_profile(self, quality, device="cpu", torch_free=None):
        sample = self.snapshot("image_profile")
        ram = sample["ram_usable"]
        available = (max(0, torch_free - MIN_GPU_HEADROOM)
                     if device == "cuda" and torch_free is not None else
                     max(0, sample["gpu_free"] - MIN_GPU_HEADROOM) if device == "cuda" else ram)
        if sample.get("on_battery"):
            available = int(available * BATTERY_RESOURCE_FRACTION)
            ram = int(ram * BATTERY_RESOURCE_FRACTION)
        return image_resource_profile(quality, device, ram, max(0, available))

    def ensure(self, stage, required=0, disk_required=0):
        sample = self.snapshot(stage)
        if required and sample["ram_usable"] < required:
            raise RuntimeError("可用内存不足，已保护系统并停止当前步骤：%s" % stage)
        if disk_required and sample["disk_free"] is not None and sample["disk_free"] < disk_required:
            raise RuntimeError("工作目录磁盘空间不足，已停止写入：%s" % stage)
        return sample

    def report(self):
        with self._lock:
            return {"peak_ram_pressure": round(self.peak_ram_pressure, 4),
                    "minimum_available_ram": self.lowest_available_ram,
                    "minimum_available_gpu": self.lowest_available_gpu,
                    "resource_stop_reason": self.resource_stop_reason,
                    "power": dict(self._power), "cpu_busy": self._cpu_busy,
                    "pressure_events": list(self.pressure_events), "samples": list(self.samples)}

def torch_install_sources(gpu, package_indexes):
    sources = []
    match = re.match(r"^(\d+)", str(gpu.get("driver", "")))
    major = int(match.group(1)) if match else 0
    if gpu.get("total_mb", 0) >= CUDA_MIN_TOTAL_MB:
        if major >= 570:
            sources.append(("CUDA 12.8", TORCH_WHEEL_INDEX + "/cu128", True))
        if major >= 560:
            sources.append(("CUDA 12.6", TORCH_WHEEL_INDEX + "/cu126", True))
        if major >= 520:
            sources.append(("CUDA 11.8", TORCH_WHEEL_INDEX + "/cu118", True))
    sources.append(("CPU", TORCH_WHEEL_INDEX + "/cpu", False))
    sources.extend(("CPU 备用源", index, False) for index in package_indexes)
    return sources


def image_resource_profile(quality, device, available_ram, available_gpu):
    available = max(0, int(available_gpu if device == "cuda" else available_ram))
    if device == "cuda":
        bounds = ((3 * GB, 256), (5 * GB, 320), (8 * GB, 448),
                  (12 * GB, 512), (16 * GB, 640), (24 * GB, 768),
                  (32 * GB, 896), (40 * GB, 1024))
    else:
        bounds = ((3 * GB, 256), (6 * GB, 320), (10 * GB, 384),
                  (16 * GB, 448), (24 * GB, 512))
    side = bounds[0][1]
    for floor, size in bounds:
        if available >= floor:
            side = size
    if quality == "快速":
        side = min(side, 448)
    elif quality == "精细" and available >= (12 if device == "cuda" else 16) * GB:
        side = min(1024, round(side * 1.12 / 8) * 8)
    steps = {"快速": 8, "智能": 16, "精细": 26}.get(quality, 16)
    if device == "cpu":
        steps = min(steps, 18)
    return max(MIN_IMAGE_DIMENSION, side // 8 * 8), steps


def is_memory_error(error):
    if isinstance(error, MemoryError):
        return True
    description = str(error).lower()
    return any(item in description for item in (
        "out of memory", "not enough memory", "cuda error: out", "cuda out of memory",
        "defaultcpuallocator", "can't allocate memory", "cannot allocate memory",
        "allocation failed", "failed to allocate", "bad allocation"))


def set_low_priority():
    try:
        if os.name == "nt":
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
        else:
            os.nice(5)
    except (OSError, AttributeError):
        pass


def configure_environment(root):
    root = Path(root)
    directories = ("models", "cache", "cache/hf", "cache/torch", "cache/pip", "jobs", "sources", "logs", "tmp")
    for dirname in directories:
        (root / ".studio" / dirname).mkdir(parents=True, exist_ok=True)
    os.environ.update({
        "HF_HOME": str(root / ".studio" / "cache" / "hf"),
        "HUGGINGFACE_HUB_CACHE": str(root / ".studio" / "cache" / "hf" / "hub"),
        "HF_XET_CACHE": str(root / ".studio" / "cache" / "hf" / "xet"),
        "TORCH_HOME": str(root / ".studio" / "cache" / "torch"),
        "PIP_CACHE_DIR": str(root / ".studio" / "cache" / "pip"),
        "TEMP": str(root / ".studio" / "tmp"),
        "TMP": str(root / ".studio" / "tmp"),
        "TMPDIR": str(root / ".studio" / "tmp"),
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "HF_HUB_DISABLE_XET": "1",
        "DO_NOT_TRACK": "1",
        "PYTHONUTF8": "1",
        "TOKENIZERS_PARALLELISM": "false",
        "PYTHONNOUSERSITE": "1",
    })
    return root / ".studio"


def runtime_python(root):
    runtime = Path(root) / ".studio" / "venv"
    return runtime / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def system_power_state():
    if os.name != "nt":
        return {"on_battery": False, "percent": None}
    class PowerStatus(ctypes.Structure):
        _fields_ = [("ac", ctypes.c_ubyte), ("flag", ctypes.c_ubyte),
                    ("percent", ctypes.c_ubyte), ("reserved", ctypes.c_ubyte),
                    ("lifetime", ctypes.c_ulong), ("remaining", ctypes.c_ulong)]
    status = PowerStatus()
    try:
        if not ctypes.windll.kernel32.GetSystemPowerStatus(ctypes.byref(status)):
            return {"on_battery": False, "percent": None}
        return {"on_battery": status.ac == 0,
                "percent": status.percent if status.percent <= 100 else None}
    except (AttributeError, OSError, ValueError):
        return {"on_battery": False, "percent": None}


def cpu_time_sample():
    if os.name != "nt":
        return None
    idle, kernel, user = ctypes.c_ulonglong(), ctypes.c_ulonglong(), ctypes.c_ulonglong()
    try:
        if not ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            return None
        return idle.value, kernel.value + user.value
    except (AttributeError, OSError):
        return None


def runtime_matches_host(root):
    executable = runtime_python(root)
    if not executable.is_file():
        return False
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    program = ("import sys,struct,json;print(json.dumps([sys.version_info[0],"
               "sys.version_info[1],struct.calcsize('P')*8]))")
    try:
        result = subprocess.run([str(executable), "-c", program], capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=18,
                                creationflags=creationflags)
        lines = result.stdout.strip().splitlines()
        return result.returncode == 0 and bool(lines) and json.loads(lines[-1]) == [
            sys.version_info.major, sys.version_info.minor, 64 if sys.maxsize > 2 ** 32 else 32]
    except (OSError, subprocess.TimeoutExpired, ValueError, IndexError):
        return False


def recover_runtime_transaction(root):
    folder = Path(root) / ".studio"
    existing = folder / "venv"
    backup = folder / RUNTIME_BACKUP_FOLDER
    if not backup.is_dir():
        return False
    if existing.exists():
        shutil.rmtree(existing)
    os.replace(backup, existing)
    return True


def installation_disk_budget(root, tier="basic", needs_piper=False, replacement=False):
    root = Path(root)
    free = shutil.disk_usage(root).free
    missing = [spec[2] for spec in MODEL_SPECS[:1 if tier == "basic" else len(MODEL_SPECS)]
               if not model_download_complete(root, spec)]
    if needs_piper and not voice_download_complete(root):
        missing.append("voice")
    expected_models = sum(MODEL_SIZE_ESTIMATES.get(name, GB) for name in missing)
    existing_venv = root / ".studio" / "venv"
    occupied = sum(file.stat().st_size for file in existing_venv.rglob("*") if file.is_file()) if existing_venv.is_dir() else 0
    engine = (5 * GB if gpu_info().get("total_mb", 0) >= CUDA_MIN_TOTAL_MB else 3 * GB)
    library_cost = GB if tier == "basic" else 2 * GB
    required = (MIN_JOB_FREE + MIN_DISK_CACHE_RESERVE +
                int(expected_models * DOWNLOAD_SPACE_MULTIPLIER) +
                (engine + library_cost if replacement or not existing_venv.is_dir() else library_cost))
    return {"free": free, "required": required, "missing_models": missing,
            "runtime_bytes": occupied, "replacement": replacement,
            "tier": tier, "estimated_model_bytes": expected_models}


def runtime_site(root):
    runtime = Path(root) / ".studio" / "venv"
    if os.name == "nt":
        return runtime / "Lib" / "site-packages"
    return runtime / "lib" / ("python%d.%d" % sys.version_info[:2]) / "site-packages"


class WorkspaceLock:
    def __init__(self, root):
        base = Path(root) / ".studio"
        base.mkdir(parents=True, exist_ok=True)
        self.handle = (base / "instance.lock").open("a+b")
        try:
            self.handle.seek(0)
            if not self.handle.read(1):
                self.handle.seek(0)
                self.handle.write(b"0")
                self.handle.flush()
            self.handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError):
            self.handle.close()
            raise RuntimeError("此工作目录正被另一个程序实例使用，请勿重复打开")

    def close(self):
        if self.handle.closed:
            return
        self.handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(self.handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        finally:
            self.handle.close()


class StopSignal:
    def __init__(self, filename):
        self.filename = Path(filename)

    def is_set(self):
        return self.filename.is_file()


def model_path(root, folder):
    return Path(root) / ".studio" / "models" / folder


def voice_model_path(root):
    return model_path(root, "voice") / VOICE_FILE


def voice_model_ready(root):
    weight = voice_model_path(root)
    config = read_json(str(weight) + ".json", {})
    return (weight.is_file() and weight.stat().st_size >= 30 * 1024 * 1024
            and isinstance(config, dict) and config.get("phoneme_type") == "espeak"
            and isinstance(config.get("phoneme_id_map"), dict)
            and bool(config.get("phoneme_id_map")))


def voice_download_complete(root, deep=False):
    marker = read_json(model_path(root, "voice") / "download.json", {})
    if not (marker.get("repo") == VOICE_REPO
            and marker.get("revision") == VOICE_REVISION
            and marker.get("sha256") == VOICE_SHA256
            and voice_model_ready(root)):
        return False
    weight = voice_model_path(root)
    if deep or not marker.get("sample_hash"):
        return full_file_sha256(weight) == VOICE_SHA256
    return marker.get("sample_hash") == file_integrity_hash(weight)


def folder_has_weights(path):
    path = Path(path)
    name = path.name.removesuffix(".downloading")
    def weighted(folder):
        return any(file.is_file() and file.stat().st_size > MODEL_CHECK_MIN_BYTES
                   for suffix in ("*.bin", "*.safetensors") for file in folder.glob(suffix))
    if name == "painter":
        if not (path / "model_index.json").is_file():
            return False
        for component in ("unet", "vae", "text_encoder"):
            folder = path / component
            if not (folder / "config.json").is_file() or not weighted(folder):
                return False
        return (path / "tokenizer" / "vocab.json").is_file() and (path / "tokenizer" / "merges.txt").is_file()
    required = {"director": ("config.json", "tokenizer_config.json"),
                "listener": ("config.json", "preprocessor_config.json"),
                "inspector": ("config.json", "preprocessor_config.json")}.get(name)
    if not required or not all((path / filename).is_file() for filename in required):
        return False
    return weighted(path)


def model_files_manifest(folder):
    folder = Path(folder)
    return {entry.relative_to(folder).as_posix(): entry.stat().st_size
            for entry in folder.rglob("*")
            if entry.is_file() and ".cache" not in entry.relative_to(folder).parts
            and entry.name != "download.json"}


def pinned_model_weights_valid(folder, repo, hashes=None, deep=False):
    folder = Path(folder)
    expected = TRUSTED_MODEL_WEIGHTS.get(repo)
    if not expected:
        return False
    if hashes is not None and not isinstance(hashes, dict):
        return False
    for relative, digest in expected.items():
        item = folder.joinpath(*PurePosixPath(relative).parts)
        if not item.is_file() or item.is_symlink() or item.stat().st_size < MODEL_CHECK_MIN_BYTES:
            return False
        if hashes is not None and not secrets.compare_digest(str(hashes.get(relative, "")), digest):
            return False
        if deep and not secrets.compare_digest(full_file_sha256(item), digest):
            return False
    return True


def file_integrity_hash(path):
    path = Path(path)
    size = path.stat().st_size
    digest = hashlib.sha256(struct.pack("<Q", size))
    with path.open("rb") as stream:
        if size <= MODEL_HASH_SAMPLE_BYTES * 3:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        else:
            for offset in (0, max(0, (size - MODEL_HASH_SAMPLE_BYTES) // 2),
                           max(0, size - MODEL_HASH_SAMPLE_BYTES)):
                stream.seek(offset)
                digest.update(struct.pack("<Q", offset))
                digest.update(stream.read(MODEL_HASH_SAMPLE_BYTES))
    return digest.hexdigest()


def full_file_sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def model_integrity_manifest(folder):
    folder = Path(folder)
    return {path.relative_to(folder).as_posix(): file_integrity_hash(path)
            for path in folder.rglob("*") if path.is_file()
            and ".cache" not in path.relative_to(folder).parts
            and path.suffix.lower() in MODEL_INTEGRITY_EXTENSIONS
            and path.name != "download.json"}


def model_full_sha256_manifest(folder):
    folder = Path(folder)
    return {path.relative_to(folder).as_posix(): full_file_sha256(path)
            for path in folder.rglob("*") if path.is_file()
            and ".cache" not in path.relative_to(folder).parts
            and path.name != "download.json"}

def git_blob_sha1(path):
    size = Path(path).stat().st_size
    digest = hashlib.sha1(("blob %d\0" % size).encode("ascii"))
    with Path(path).open("rb") as stream:
        for piece in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(piece)
    return digest.hexdigest()


def official_model_metadata(repo, revision, endpoint):
    from huggingface_hub import HfApi
    tried = []
    for server in ("https://huggingface.co",):
        try:
            info = HfApi(endpoint=server).model_info(repo_id=repo, revision=revision,
                                                      files_metadata=True, timeout=SOURCE_METADATA_TIMEOUT)
            if info.sha != revision:
                raise RuntimeError("模型仓库提交版本与锁定值不一致")
            hashes = {}
            sizes = {}
            for sibling in info.siblings:
                name = str(sibling.rfilename)
                size = getattr(sibling, "size", None)
                if isinstance(size, int) and size >= 0:
                    sizes[name] = size
                lfs = getattr(sibling, "lfs", None)
                value = lfs.get("sha256") if isinstance(lfs, dict) else None
                if value and re.fullmatch(r"[0-9a-f]{64}", value):
                    hashes[name] = {"type": "sha256", "value": value}
                else:
                    blob = getattr(sibling, "blob_id", None)
                    if isinstance(blob, str) and re.fullmatch(r"[0-9a-f]{40}", blob):
                        hashes[name] = {"type": "git-sha1", "value": blob}
            if not hashes:
                raise RuntimeError("仓库未返回可校验的文件摘要")
            pinned = TRUSTED_MODEL_WEIGHTS.get(repo, {})
            if any(hashes.get(name, {}).get("value") != digest and hashes.get(name, {}).get("type") == "sha256"
                   for name, digest in pinned.items()):
                raise RuntimeError("官方固定提交权重摘要与内置可信清单冲突")
            return {"repo": repo, "revision": revision, "origin": server,
                    "authoritative": True, "hashes": hashes, "sizes": sizes}
        except (OSError, RuntimeError, ValueError, urllib.error.URLError) as error:
            tried.append(str(error)[:170])
    pins = TRUSTED_MODEL_WEIGHTS.get(repo)
    if not pins:
        raise RuntimeError("官方元数据不可访问且没有独立的可信权重摘要：" + " / ".join(tried))
    print("官方元数据暂不可达，启用程序内置可信 SHA-256 权重校验；镜像配置文件仍需离线推理验收", flush=True)
    return {"repo": repo, "revision": revision, "origin": "embedded-sha256-pins",
            "authoritative": False, "verification_level": "pinned_weights_only",
            "hashes": {name: {"type": "sha256", "value": value} for name, value in pins.items()},
            "sizes": {}, "official_errors": tried[-2:]}


def verify_remote_file_hashes(folder, provenance, mandatory=True):
    hashes = provenance.get("hashes", {})
    if not isinstance(hashes, dict):
        return False
    checked = 0
    for name, value in hashes.items():
        if not isinstance(name, str) or Path(name).is_absolute() or ".." in Path(name).parts:
            return False
        file = Path(folder) / name
        if not file.is_file():
            continue
        if not isinstance(value, dict) or value.get("type") not in {"sha256", "git-sha1"}:
            return False
        expected = value.get("value", "")
        if (value["type"] == "git-sha1" and
                name in TRUSTED_MODEL_WEIGHTS.get(provenance.get("repo", ""), {})):
            if full_file_sha256(file) != TRUSTED_MODEL_WEIGHTS[provenance["repo"]][name]:
                return False
            checked += 1
            continue
        actual = full_file_sha256(file) if value["type"] == "sha256" else git_blob_sha1(file)
        if not secrets.compare_digest(str(expected), actual):
            return False
        if file.suffix.lower() in {".bin", ".safetensors", ".onnx"}:
            checked += 1
    return bool(checked) if mandatory else True


def model_folder_complete(folder, spec, deep=False):
    repo = spec[1]
    folder = Path(folder)
    marker = read_json(folder / "download.json", {})
    if (not folder_has_weights(folder) or marker.get("repo") != repo
            or marker.get("revision") != MODEL_REVISIONS.get(repo)
            or not marker.get("complete")):
        return False
    recorded = marker.get("files")
    if not isinstance(recorded, dict) or not recorded:
        return False
    for relative, size in recorded.items():
        if not isinstance(relative, str) or not isinstance(size, int) or size <= 0:
            return False
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts:
            return False
        item = folder / path
        if not item.is_file() or item.stat().st_size != size:
            return False
    full_hashes = marker.get("sha256")
    if not isinstance(full_hashes, dict) or set(full_hashes) != set(recorded):
        return False
    if any(not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
           for value in full_hashes.values()):
        return False
    if not pinned_model_weights_valid(folder, repo, full_hashes, deep=deep):
        return False
    integrity = marker.get("integrity")
    if not isinstance(integrity, dict) or not integrity:
        return False
    for relative, signature in integrity.items():
        if (relative not in recorded or not isinstance(relative, str)
                or not re.fullmatch(r"[0-9a-f]{64}", str(signature))
                or Path(relative).is_absolute() or ".." in Path(relative).parts):
            return False
        item = folder / relative
        if not item.is_file() or file_integrity_hash(item) != signature:
            return False
    if deep:
        for relative, digest in full_hashes.items():
            if full_file_sha256(folder / relative) != digest:
                return False
        provenance = marker.get("source_metadata")
        if provenance:
            if (not isinstance(provenance, dict) or provenance.get("repo") != repo or
                    provenance.get("revision") != MODEL_REVISIONS[repo]):
                return False
            official = (provenance.get("authoritative") is True and
                        provenance.get("origin") == "https://huggingface.co")
            embedded = (provenance.get("authoritative") is False and
                        provenance.get("origin") == "embedded-sha256-pins" and
                        provenance.get("verification_level") == "pinned_weights_only" and
                        provenance.get("hashes") == {name: {"type": "sha256", "value": value}
                                                      for name, value in TRUSTED_MODEL_WEIGHTS[repo].items()})
            if not (official or embedded) or not verify_remote_file_hashes(folder, provenance):
                return False
    for index in folder.rglob("*.index.json"):
        index_data = read_json(index, {})
        weights = index_data.get("weight_map")
        if not isinstance(weights, dict) or not weights:
            return False
        for relative in set(weights.values()):
            if not isinstance(relative, str) or ".." in Path(relative).parts:
                return False
            shard = index.parent / relative
            if not shard.is_file() or shard.stat().st_size <= MODEL_CHECK_MIN_BYTES:
                return False
    return True


def remove_corrupt_model_files(folder, marker):
    folder = Path(folder)
    hashes = marker.get("sha256", {})
    sizes = marker.get("files", {})
    signatures = marker.get("integrity", {})
    for relative, size in sizes.items():
        if not isinstance(relative, str) or Path(relative).is_absolute() or ".." in Path(relative).parts:
            continue
        path = folder / relative
        if not path.is_file():
            continue
        corrupted = (path.stat().st_size != size or
                     relative in signatures and file_integrity_hash(path) != signatures[relative] or
                     relative in hashes and full_file_sha256(path) != hashes[relative])
        if corrupted:
            path.unlink()


def optional_model_verified(folder, role, deep=False):
    folder = Path(folder)
    manifest = read_json(folder / "download.json", {})
    if (role not in OPTIONAL_MODEL_FOLDERS or manifest.get("role") != role
            or not manifest.get("complete") or not isinstance(manifest.get("sha256"), dict)
            or not manifest.get("source_metadata")):
        return False
    weights = [part for ext in ("*.bin", "*.safetensors") for part in folder.rglob(ext)]
    if not weights or not (folder / ("model_index.json" if role == "painter" else "config.json")).is_file():
        return False
    signatures = manifest["sha256"]
    checked_integrity = manifest.get("integrity", {})
    if not isinstance(checked_integrity, dict) or not checked_integrity:
        return False
    if not all((entry.relative_to(folder).as_posix() in signatures) for entry in weights):
        return False
    for relative, digest in signatures.items():
        filename = Path(relative)
        if filename.is_absolute() or ".." in filename.parts or not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            return False
        item = folder / filename
        if not item.is_file():
            return False
        if relative in checked_integrity and file_integrity_hash(item) != checked_integrity[relative]:
            return False
        if deep and full_file_sha256(item) != digest:
            return False
    if not set(weight.relative_to(folder).as_posix() for weight in weights).issubset(checked_integrity):
        return False
    return not deep or verify_remote_file_hashes(folder, manifest["source_metadata"])


def model_provenance(root):
    result = []
    for _, repo, folder, _ in MODEL_SPECS:
        marker = read_json(model_path(root, folder) / "download.json", {})
        origin = marker.get("source_metadata", {})
        result.append({"role": folder, "repo": repo, "revision_locked": marker.get("revision") == MODEL_REVISIONS[repo],
                       "source_metadata": "official" if origin.get("authoritative") else
                       "mirror_only" if origin.get("hashes") else "self_hash_only",
                       "content_verified": bool(origin.get("hashes"))})
    return result


def model_download_complete(root, spec, deep=False):
    return model_folder_complete(model_path(root, spec[2]), spec, deep=deep)


def models_complete(root):
    return all(model_download_complete(root, item) for item in MODEL_SPECS)


def required_imports(tier, needs_piper=False):
    result = dict(CORE_PACKAGE_IMPORTS)
    if tier == "full":
        result.update(EXTENDED_PACKAGE_IMPORTS)
    if needs_piper:
        result["piper-tts"] = "piper"
    return result


def installed_package_versions(root):
    site = runtime_site(root)
    versions = {}
    if site.is_dir():
        for item in importlib.metadata.distributions(path=[str(site)]):
            name = str(item.metadata.get("Name", "")).strip().lower().replace("_", "-")
            if name:
                versions[name] = item.version
    return versions


def package_sentinels(root, tier, needs_piper=False):
    site = runtime_site(root)
    result = {}
    for module in required_imports(tier, needs_piper).values():
        folder = site / module
        candidate = folder / "__init__.py" if folder.is_dir() else site / (module + ".py")
        if not candidate.is_file():
            return None
        result[candidate.relative_to(site).as_posix()] = file_integrity_hash(candidate)
    binary = site / "torch" / ("_C.pyd" if os.name == "nt" else "_C" + (".so" if sys.platform != "darwin" else ".dylib"))
    if binary.is_file():
        result[binary.relative_to(site).as_posix()] = file_integrity_hash(binary)
    return result


def optional_ocr_ready(root):
    marker = read_json(Path(root) / ".studio" / "ocr_ready.json", {})
    if (marker.get("runtime_version") != RUNTIME_VERSION or
            marker.get("python") != list(sys.version_info[:2])):
        return False
    installed = installed_package_versions(root)
    return all(installed.get(name) == marker.get("versions", {}).get(name)
               and (runtime_site(root) / module / "__init__.py").is_file()
               for name, module in OPTIONAL_OCR_PACKAGE_IMPORTS.items())


def packages_healthy(root, tier="basic", needs_piper=False):
    marker = read_json(Path(root) / ".studio" / "packages_ready.json", {})
    if (marker.get("runtime_version") != RUNTIME_VERSION or
            marker.get("python") != list(sys.version_info[:2]) or
            not marker.get("tiers", {}).get(tier) or not runtime_matches_host(root)):
        return False
    expected = required_imports(tier, needs_piper)
    versions = installed_package_versions(root)
    locked = marker.get("versions", {})
    if any(not versions.get(name) or versions[name] != locked.get(name) for name in expected):
        return False
    expected_signatures = marker.get("sentinels", {})
    current = package_sentinels(root, tier, needs_piper)
    return bool(current) and all(expected_signatures.get(name) == value for name, value in current.items())


def verify_packages_worker(root, tier="basic", needs_piper=False):
    configure_environment(root)
    imported = {}
    if tier == "ocr":
        for distribution, module in OPTIONAL_OCR_PACKAGE_IMPORTS.items():
            imported[distribution] = importlib.import_module(module).__name__
        from rapidocr import RapidOCR
        if not callable(RapidOCR):
            raise RuntimeError("离线 OCR 模块无法创建")
        print(json.dumps({"ok": True, "tier": tier, "imports": imported}, ensure_ascii=False), flush=True)
        return
    for distribution, module in required_imports(tier, needs_piper).items():
        imported[distribution] = importlib.import_module(module).__name__
    import torch
    if not math.isclose(float(torch.ones(2, device="cpu").sum().item()), 2.0):
        raise RuntimeError("PyTorch CPU 计算校验失败")
    if tier == "full":
        from diffusers import DiffusionPipeline
        from transformers import CLIPModel, WhisperForConditionalGeneration
        if not all((DiffusionPipeline, CLIPModel, WhisperForConditionalGeneration)):
            raise RuntimeError("离线模型的导入检查失败")
    print(json.dumps({"ok": True, "tier": tier, "imports": imported}, ensure_ascii=False), flush=True)


def basic_ready(root):
    marker = read_json(Path(root) / ".studio" / "basic_ready.json", {})
    if (marker.get("runtime_version") != RUNTIME_VERSION
            or marker.get("python") != list(sys.version_info[:2])
            or not marker.get("diagnostic", {}).get("smoke_test")
            or not runtime_matches_host(root)):
        return False
    if not model_download_complete(root, MODEL_SPECS[0]):
        return False
    voice_backend = marker.get("diagnostic", {}).get("voice_backend")
    if voice_backend not in {"sapi", "piper"} or not voice_backend_operational(root, voice_backend):
        return False
    return packages_healthy(root, "basic", voice_backend == "piper")


def safetensors_structure_valid(path):
    path = Path(path)
    try:
        size = path.stat().st_size
        if size <= 32:
            return False
        with path.open("rb") as stream:
            header_size = struct.unpack("<Q", stream.read(8))[0]
            if not 2 <= header_size <= min(size - 8, 64 * 1024 * 1024):
                return False
            header = json.loads(stream.read(header_size).decode("utf-8"))
        if not isinstance(header, dict):
            return False
        entries = [entry for key, entry in header.items() if key != "__metadata__"]
        if not entries:
            return False
        payload_size = size - 8 - header_size
        for value in entries:
            if not isinstance(value, dict):
                return False
            offsets = value.get("data_offsets")
            if (not isinstance(offsets, list) or len(offsets) != 2 or
                    not all(isinstance(number, int) for number in offsets) or
                    not 0 <= offsets[0] < offsets[1] <= payload_size or
                    not isinstance(value.get("dtype"), str) or
                    not isinstance(value.get("shape"), list)):
                return False
        return True
    except (OSError, ValueError, TypeError, UnicodeError, struct.error, OverflowError):
        return False


def native_component_layout_valid(folder):
    folder = Path(folder)
    info = read_json(folder / "model_index.json", {})
    if info.get("_class_name") not in {"CogVideoXPipeline", "CogVideoXImageToVideoPipeline"}:
        return False
    for component in NATIVE_COMPONENTS:
        entry = info.get(component)
        if not isinstance(entry, list) or len(entry) != 2 or not all(isinstance(x, str) for x in entry):
            return False
        base = folder / component
        if not base.is_dir():
            return False
        config_name = ("scheduler_config.json" if component == "scheduler" else
                       "tokenizer_config.json" if component == "tokenizer" else "config.json")
        if not (base / config_name).is_file():
            return False
        if component == "tokenizer" and not any(
                (base / name).is_file() for name in
                ("tokenizer.json", "spiece.model", "sentencepiece.bpe.model", "vocab.json", "vocab.txt")):
            return False
        if component in {"transformer", "vae", "text_encoder"}:
            weights = [path for path in base.rglob("*") if path.is_file() and
                       path.suffix.lower() in {".safetensors", ".bin"}]
            if sum(path.stat().st_size for path in weights) < MODEL_CHECK_MIN_BYTES or not all(
                    (safetensors_structure_valid(path) if path.suffix.lower() == ".safetensors" else
                     path.stat().st_size >= MODEL_CHECK_MIN_BYTES) for path in weights):
                return False
    for index in folder.rglob("*.index.json"):
        records = read_json(index, {})
        weight_map = records.get("weight_map", {})
        if not isinstance(weight_map, dict) or not weight_map:
            return False
        for name in set(weight_map.values()):
            if not isinstance(name, str):
                return False
            part = PurePosixPath(name)
            if part.is_absolute() or ".." in part.parts or len(part.parts) != 1:
                return False
            shard = index.parent / name
            if not shard.is_file() or shard.stat().st_size < MODEL_CHECK_MIN_BYTES:
                return False
    return True


def native_video_folder_complete(folder, deep=False):
    folder = Path(folder)
    if not native_component_layout_valid(folder):
        return False
    marker = read_json(folder / "download.json", {})
    if marker.get("kind") != "cogvideox" or marker.get("complete") is not True:
        return False
    files = marker.get("files")
    hashes = marker.get("sha256")
    signatures = marker.get("integrity")
    if (not isinstance(files, dict) or not files or not isinstance(hashes, dict) or
            not isinstance(signatures, dict) or set(files) != set(hashes) or
            not set(signatures).issuperset({name for name in files if
                                             Path(name).suffix.lower() in {".bin", ".safetensors"}})):
        return False
    if set(files) != set(model_files_manifest(folder)):
        return False
    for relative, size in files.items():
        part = PurePosixPath(relative)
        if (not isinstance(relative, str) or part.is_absolute() or ".." in part.parts or
                not isinstance(size, int) or size <= 0 or
                not isinstance(hashes.get(relative), str) or
                not re.fullmatch(r"[0-9a-f]{64}", hashes[relative])):
            return False
        file = folder.joinpath(*part.parts)
        if not file.is_file() or file.stat().st_size != size:
            return False
        if relative in signatures and (not isinstance(signatures[relative], str) or
                                       file_integrity_hash(file) != signatures[relative]):
            return False
        if deep and full_file_sha256(file) != hashes[relative]:
            return False
    source = marker.get("source_metadata")
    if any(file.suffix.lower() == ".bin" for file in folder.rglob("*.bin")):
        if not isinstance(source, dict) or not source.get("authoritative"):
            return False
        if not verify_remote_file_hashes(folder, source):
            return False
    if deep and source and not verify_remote_file_hashes(folder, source):
        return False
    return True


def native_video_model(root):
    folder = model_path(root, VIDEO_MODEL_FOLDER)
    if not native_video_folder_complete(folder):
        return None
    return folder, read_json(folder / "model_index.json", {})["_class_name"]


def native_model_signature(root):
    folder = model_path(root, VIDEO_MODEL_FOLDER)
    marker = read_json(folder / "download.json", {})
    paths = sorted((name, digest) for name, digest in marker.get("sha256", {}).items())
    return hashlib.sha256(json.dumps(paths, ensure_ascii=False).encode("utf-8")).hexdigest()


def native_load_ready(root):
    model = native_video_model(root)
    if model is None:
        return False
    marker = read_json(Path(root) / ".studio" / "native_ready.json", {})
    devices = gpu_info().get("devices", [])
    matching = any(item.get("name") == marker.get("gpu_name") and
                   abs(item.get("total_mb", 0) - marker.get("gpu_total_mb", 0)) <=
                   max(256, int(marker.get("gpu_total_mb", 0) * .04)) for item in devices)
    return bool(marker.get("runtime_version") == RUNTIME_VERSION and
                marker.get("python") == list(sys.version_info[:2]) and
                marker.get("model_signature") == native_model_signature(root) and
                marker.get("model_class") == model[1] and
                marker.get("offline_load") is True and matching)


def native_inference_ready(root):
    marker = read_json(Path(root) / ".studio" / "native_ready.json", {})
    return bool(native_load_ready(root) and marker.get("inference_tested") is True and
                marker.get("decode_tested") is True and marker.get("frame_count", 0) >= NATIVE_SMOKE_FRAMES)


def native_gpu_snapshot(root):
    marker = read_json(Path(root) / ".studio" / "native_ready.json", {})
    devices = gpu_info().get("devices", [])
    eligible = [item for item in devices if item.get("name") == marker.get("gpu_name") and
                abs(item.get("total_mb", 0) - marker.get("gpu_total_mb", 0)) <=
                max(256, int(marker.get("gpu_total_mb", 0) * .04))]
    selected = next((item for item in eligible if item["index"] == marker.get("gpu_index")), None)
    return selected or {}


def check_native_worker(root):
    configure_environment(root)
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "DIFFUSERS_OFFLINE": "1"})
    model = native_video_model(root)
    if not model or not native_video_folder_complete(model[0], deep=True):
        raise RuntimeError("原生模型在离线加载前未通过完整文件 SHA-256 与组件检查")
    import torch
    from diffusers import CogVideoXPipeline, CogVideoXImageToVideoPipeline
    from diffusers.utils import export_to_video
    from PIL import Image
    set_low_priority()
    ResourceGovernor(root).budget("native_model_offline_load", ram_bytes=MIN_SYSTEM_MEMORY_HEADROOM)
    gpu = select_torch_gpu(torch, NATIVE_VIDEO_MIN_FREE_MB * 1024 * 1024)
    if gpu is None:
        raise RuntimeError("当前可见的 NVIDIA GPU 显存不足，原生视频保持未验收状态")
    torch.cuda.set_device(gpu["index"])
    cls = CogVideoXImageToVideoPipeline if model[1] == "CogVideoXImageToVideoPipeline" else CogVideoXPipeline
    marker_file = Path(root) / ".studio" / "native_ready.json"
    marker = {"runtime_version": RUNTIME_VERSION, "python": list(sys.version_info[:2]),
              "model_signature": native_model_signature(root), "model_class": model[1],
              "gpu_name": gpu["name"], "gpu_total_mb": gpu["total_mb"],
              "gpu_index": gpu["index"], "offline_load": False,
              "inference_tested": False, "decode_tested": False, "frame_count": 0,
              "checked": datetime.datetime.now().isoformat()}
    pipeline = None
    probe_video = Path(root) / ".studio" / "tmp" / "native_inference_probe.mp4"
    try:
        pipeline = cls.from_pretrained(str(model[0]), local_files_only=True,
                                       torch_dtype=native_model_precision(torch, gpu["index"]))
        for role in NATIVE_COMPONENTS:
            if getattr(pipeline, role, None) is None:
                raise RuntimeError("原生视频模型加载后缺少组件：" + role)
        pipeline.enable_model_cpu_offload(gpu_id=gpu["index"])
        if hasattr(pipeline, "vae") and hasattr(pipeline.vae, "enable_tiling"):
            pipeline.vae.enable_tiling()
        marker["offline_load"] = True
        atomic_json(marker_file, marker)
        width, height = NATIVE_RESOLUTIONS["横屏"][-1]
        params = {"prompt": "a red cube slowly rotating, cinematic lighting", "width": width,
                  "height": height, "num_frames": NATIVE_SMOKE_FRAMES,
                  "num_inference_steps": NATIVE_SMOKE_STEPS, "guidance_scale": 1.0}
        if model[1] == "CogVideoXImageToVideoPipeline":
            params["image"] = Image.new("RGB", (width, height), (170, 38, 45))
        with torch.inference_mode():
            frames = pipeline(**params).frames[0]
        if not isinstance(frames, (list, tuple)) or len(frames) < NATIVE_SMOKE_FRAMES:
            raise RuntimeError("原生模型未生成完整的测试帧")
        export_to_video(frames, str(probe_video), fps=NATIVE_VIDEO_FPS)
        if not probe_video.is_file() or probe_video.stat().st_size < 8192:
            raise RuntimeError("原生模型测试视频编码结果无效")
        run_external([ffmpeg_executable(), "-hide_banner", "-loglevel", "error", "-xerror",
                      "-i", str(probe_video), "-f", "null", "-"], root,
                     timeout=120, env=shell_env(root, offline=True), capture=True)
        marker.update({"inference_tested": True, "decode_tested": True,
                       "frame_count": len(frames), "smoke_status": REVIEW_PASS})
        atomic_json(marker_file, marker)
        print(json.dumps({"ok": True, "offline_load": True, "inference_tested": True,
                          "decode_tested": True, "model_class": model[1]}, ensure_ascii=False), flush=True)
    except (RuntimeError, MemoryError, OSError, ValueError) as error:
        marker.update({"smoke_status": REVIEW_UNAVAILABLE,
                       "smoke_error_type": type(error).__name__,
                       "smoke_error_code": "RESOURCE_EXHAUSTED" if is_memory_error(error) else "NATIVE_INFERENCE_FAILED"})
        atomic_json(marker_file, marker)
        raise RuntimeError("原生模型已加载但真实推理或解码尚未通过：" + type(error).__name__) from error
    finally:
        probe_video.unlink(missing_ok=True)
        del pipeline
        gc.collect()
        torch.cuda.empty_cache()

def model_signature(root):
    entries = []
    for _, _, folder, _ in MODEL_SPECS:
        base = model_path(root, folder)
        for item in base.rglob("*"):
            if not item.is_file() or ".cache" in item.parts:
                continue
            if item.suffix.lower() not in {".json", ".txt", ".model", ".bin", ".safetensors"}:
                continue
            stat = item.stat()
            entries.append((folder, item.relative_to(base).as_posix(), stat.st_size, stat.st_mtime_ns))
    for role, folder in OPTIONAL_MODEL_FOLDERS.items():
        path = model_path(root, folder)
        if optional_model_verified(path, role):
            marker = read_json(path / "download.json", {})
            entries.append((folder, "verified_extra", marker.get("revision", ""),
                            len(marker.get("sha256", {}))))
    if native_video_model(root):
        entries.append((VIDEO_MODEL_FOLDER, "verified_native", native_model_signature(root), 1))
    return hashlib.sha256(json.dumps(sorted(entries)).encode("utf-8")).hexdigest()


def shell_env(root, offline=False, endpoint=None):
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONUTF8"] = "1"
    env["PYTHONNOUSERSITE"] = "1"
    env["HF_HOME"] = str(Path(root) / ".studio" / "cache" / "hf")
    env["HF_HUB_CACHE"] = str(Path(root) / ".studio" / "cache" / "hf" / "hub")
    env["HF_XET_CACHE"] = str(Path(root) / ".studio" / "cache" / "hf" / "xet")
    env["TORCH_HOME"] = str(Path(root) / ".studio" / "cache" / "torch")
    env["PIP_CACHE_DIR"] = str(Path(root) / ".studio" / "cache" / "pip")
    env["TEMP"] = str(Path(root) / ".studio" / "tmp")
    env["TMP"] = str(Path(root) / ".studio" / "tmp")
    env["TMPDIR"] = str(Path(root) / ".studio" / "tmp")
    env["HF_HUB_DISABLE_TELEMETRY"] = "1"
    env["HF_HUB_DISABLE_XET"] = "1"
    env["TOKENIZERS_PARALLELISM"] = "false"
    if offline:
        env["HF_HUB_OFFLINE"] = "1"
        env["TRANSFORMERS_OFFLINE"] = "1"
        env["DIFFUSERS_OFFLINE"] = "1"
    else:
        for key in ("HF_HUB_OFFLINE", "TRANSFORMERS_OFFLINE", "DIFFUSERS_OFFLINE"):
            env.pop(key, None)
    if endpoint:
        env["HF_ENDPOINT"] = endpoint
    return env


def is_ready(root):
    marker = read_json(Path(root) / ".studio" / "ready.json", {})
    if (not marker or marker.get("runtime_version") != RUNTIME_VERSION or not marker.get("smoke_test")
            or marker.get("python") != list(sys.version_info[:2]) or not models_complete(root)):
        return False
    if marker.get("model_signature") != model_signature(root):
        return False
    diagnostics = marker.get("diagnostic", {})
    if not diagnostics.get("chinese_voice") or diagnostics.get("voice_backend") not in {"sapi", "piper"}:
        return False
    if not voice_backend_operational(root, diagnostics["voice_backend"]):
        return False
    if not runtime_matches_host(root):
        return False
    return packages_healthy(root, "full", diagnostics["voice_backend"] == "piper")



def capability_report(root, request=None):
    root = Path(root)
    basic = basic_ready(root)
    complete = bool(basic and is_ready(root))
    native_files = native_video_model(root) if complete else None
    native_loaded = bool(native_files and native_load_ready(root))
    native_verified = bool(native_loaded and native_inference_ready(root))
    gpu = native_gpu_snapshot(root) if native_files else {}
    native_available = bool(native_verified and gpu.get("free_mb", 0) >= NATIVE_VIDEO_MIN_FREE_MB)
    files = request.get("files", {}) if isinstance(request, dict) else {}
    visual_assets = any(files.get(item) for item in ("图片", "首帧", "尾帧", "视频"))
    native_requested = bool(request and str(request.get("visual_mode", "")).startswith("原生AI视频"))
    can_create = bool(complete or basic and visual_assets)
    return {"basic": bool(basic), "image_generation": complete,
            "semantic_review": complete, "speech_review": complete,
            "ocr": optional_ocr_ready(root) if complete else False,
            "native_video": native_available, "native_inference_verified": native_verified,
            "native_model_present": (model_path(root, VIDEO_MODEL_FOLDER) / "model_index.json").is_file(),
            "native_model_detected": bool(native_files), "native_load_verified": native_loaded,
            "native_gpu_free_mb": gpu.get("free_mb", 0),
            "visual_assets": bool(visual_assets), "native_requested": native_requested,
            "create_allowed": can_create, "offline": can_create, "full_offline": complete,
            "review_level": "full" if complete else "technical_only" if can_create else "unavailable"}


def require_request_capabilities(root, request):
    capabilities = capability_report(root, request)
    if not capabilities["create_allowed"]:
        if not capabilities["basic"]:
            raise RuntimeError("基础离线分镜、配音和视频编码尚未通过验收，请完成基础部署")
        raise RuntimeError("缺少离线生图模型且未提供图片或视频，请补充画面素材或等待扩展模型部署")
    if capabilities["native_requested"] and not capabilities["native_video"]:
        request["visual_mode"] = "智能轻量运镜"
        capabilities["native_fallback"] = "原生视频未通过实际推理验收或显存不足，改用图片动态运镜"
    return capabilities

def available_threads():
    logical = os.cpu_count() or 2
    memory = memory_info()["available"]
    limit = max(1, logical - max(1, logical // 3))
    if 0 < memory < 4 * GB:
        limit = min(limit, 2)
    elif 0 < memory < 8 * GB:
        limit = min(limit, 4)
    return max(1, min(8, limit))


def stop_process_tree(proc):
    if proc.poll() is not None:
        return
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                           capture_output=True, timeout=6, creationflags=subprocess.CREATE_NO_WINDOW)
        except (OSError, subprocess.TimeoutExpired):
            pass
    if proc.poll() is None:
        try:
            proc.terminate()
            proc.wait(timeout=2)
        except (OSError, subprocess.TimeoutExpired):
            proc.kill()


def run_external(args, root, log=None, cancel=None, timeout=None, env=None, capture=False,
                 on_line=None, stop_file=None, stop_grace=0):
    flags = (subprocess.CREATE_NO_WINDOW | 0x00004000) if os.name == "nt" else 0
    args = list(args)
    if (args and "ffmpeg" in Path(str(args[0])).name.lower() and "-threads" not in args):
        cores = max(1, os.cpu_count() or 1)
        budget_threads = max(1, min(available_threads(), int(cores * RESOURCE_MAX_CPU_SHARE)))
        args[1:1] = ["-threads", str(budget_threads), "-filter_threads", str(budget_threads)]
    if log:
        log("命令类别：" + Path(str(args[0])).name + " · " + " ".join(str(arg) for arg in args[1:3])[:110])
    started = time.monotonic()
    audit = {"tool": Path(str(args[0])).name, "purpose": str(args[1])[:75] if len(args) > 1 else "",
             "started": datetime.datetime.now().isoformat(), "timeout": timeout,
             "status": "started", "returncode": None}
    proc = subprocess.Popen([str(arg) for arg in args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            stdin=subprocess.DEVNULL, bufsize=1, text=True, encoding="utf-8", errors="replace",
                            env=env or shell_env(root), creationflags=flags, cwd=str(root))
    with RUNNING_CHILDREN_LOCK:
        RUNNING_CHILDREN.add(proc)
    output = []
    tail = deque(maxlen=EXTERNAL_ERROR_LINES)
    pending = queue.Queue(maxsize=EXTERNAL_OUTPUT_QUEUE)
    completed = threading.Event()
    abandoned = threading.Event()
    def reader():
        try:
            for message in proc.stdout:
                if abandoned.is_set():
                    break
                while not abandoned.is_set():
                    try:
                        pending.put(message, timeout=.1)
                        break
                    except queue.Full:
                        if proc.poll() is not None and abandoned.is_set():
                            break
        except (OSError, ValueError):
            pass
        finally:
            completed.set()
    thread = threading.Thread(target=reader, daemon=True)
    thread.start()
    stopping = None
    try:
        while True:
            if cancel is not None and cancel.is_set():
                if stop_file is not None and stopping is None:
                    Path(stop_file).touch()
                    stopping = time.monotonic()
                if stopping is None or time.monotonic() - stopping >= stop_grace:
                    stop_process_tree(proc)
                    raise InterruptedError("已停止，已保存已完成的检查点")
            if timeout and time.monotonic() - started > timeout:
                stop_process_tree(proc)
                raise TimeoutError("外部进程运行超时")
            try:
                line = pending.get(timeout=.16).rstrip()
            except queue.Empty:
                if proc.poll() is not None and completed.is_set() and pending.empty():
                    break
                continue
            if line:
                tail.append(line)
                if on_line:
                    on_line(line)
                if log:
                    log(line)
                if capture:
                    output.append(line)
                    if len(output) > 1200:
                        output = output[-800:]
        code = proc.wait()
        audit["returncode"] = code
        if stopping is not None:
            raise InterruptedError("已停止，已保存已完成的检查点")
        if code:
            raise RuntimeError("命令失败（退出码 %s）：%s" % (code, " | ".join(tail)))
        return "\n".join(output)
    finally:
        abandoned.set()
        if proc.poll() is None:
            stop_process_tree(proc)
        if proc.stdout is not None:
            try:
                proc.stdout.close()
            except OSError:
                pass
        try:
            proc.wait(timeout=3)
        except (OSError, subprocess.TimeoutExpired):
            pass
        thread.join(timeout=2)
        audit["elapsed_seconds"] = round(time.monotonic() - started, 3)
        audit["returncode"] = proc.returncode
        audit["status"] = "completed" if proc.returncode == 0 else "interrupted_or_failed"
        audit["last_output"] = " | ".join(list(tail)[-3:])[-500:]
        with EXTERNAL_COMMAND_LOCK:
            EXTERNAL_COMMAND_EVENTS.append(dict(audit))
            try:
                history = Path(root) / ".studio" / "logs" / "process_events.jsonl"
                history.parent.mkdir(parents=True, exist_ok=True)
                if history.is_file() and history.stat().st_size > 5 * 1024 * 1024:
                    history.replace(history.with_suffix(".previous.jsonl"))
                with history.open("a", encoding="utf-8") as audit_file:
                    audit_file.write(json.dumps(audit, ensure_ascii=False) + "\n")
            except OSError:
                pass
        with RUNNING_CHILDREN_LOCK:
            RUNNING_CHILDREN.discard(proc)

def probe_url(url, timeout=4):
    started = time.monotonic()
    for method in ("HEAD", "GET"):
        headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json, */*"}
        if method == "GET":
            headers["Range"] = "bytes=0-511"
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if method == "GET":
                    response.read(512)
            return time.monotonic() - started
        except (OSError, urllib.error.URLError, ValueError):
            continue
    return float("inf")


def download_disk_budget(root, folder, reserve=MIN_DISK_DOWNLOAD_RESERVE, source_metadata=None):
    root = Path(root)
    expected = MODEL_SIZE_ESTIMATES.get(folder, GB)
    if isinstance(source_metadata, dict):
        sizes = source_metadata.get("sizes", {})
        if isinstance(sizes, dict) and sizes:
            expected = sum(int(value) for name, value in sizes.items()
                           if isinstance(value, int) and value >= 0 and
                           Path(name).suffix.lower() in MODEL_INTEGRITY_EXTENSIONS)
            expected = max(MODEL_CHECK_MIN_BYTES, expected)
    existing = 0
    for dirname in (folder, folder + ".downloading"):
        path = model_path(root, dirname)
        if path.is_dir():
            existing = max(existing, sum(file.stat().st_size for file in path.rglob("*") if file.is_file()))
    remaining = max(0, expected - existing)
    needed = reserve + int(remaining * DOWNLOAD_SPACE_MULTIPLIER)
    free = shutil.disk_usage(root).free
    if free < needed:
        raise RuntimeError("下载前空间检查未通过：%s 预计至少需要 %.2f GB 可用空间（当前 %.2f GB），请更换工作目录或清理磁盘" % (
            folder, needed / GB, free / GB))
    return {"estimated_remaining": remaining, "required_free": needed, "current_free": free}


def choose_endpoints():
    possibilities = ("https://hf-mirror.com", "https://huggingface.co")
    values = {}
    threads = []
    def measure(base):
        values[base] = probe_url(base + "/api/models/openai/whisper-tiny")
    for item in possibilities:
        thread = threading.Thread(target=measure, args=(item,), daemon=True)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join(5)
    return sorted(possibilities, key=lambda item: values.get(item, float("inf")))


def download_model_worker(root, index, endpoint, deep=False):
    configure_environment(root)
    os.environ["HF_ENDPOINT"] = endpoint
    os.environ["HF_HUB_OFFLINE"] = "0"
    from huggingface_hub import snapshot_download
    spec = MODEL_SPECS[int(index)]
    target = model_path(root, spec[2])
    staging = target.with_name(target.name + ".downloading")
    if model_folder_complete(target, spec, deep=deep):
        return
    download_disk_budget(root, spec[2])
    if target.exists() and not staging.exists():
        target.replace(staging)
    staging.mkdir(parents=True, exist_ok=True)
    if model_folder_complete(staging, spec, deep=deep):
        if target.exists():
            shutil.rmtree(target)
        staging.replace(target)
        return
    revision = MODEL_REVISIONS[spec[1]]
    previous = read_json(staging / "download.json", {})
    if previous.get("repo") == spec[1] and previous.get("revision") == revision:
        remove_corrupt_model_files(staging, previous)
    elif previous:
        shutil.rmtree(staging)
        staging.mkdir(parents=True, exist_ok=True)
    source_metadata = official_model_metadata(spec[1], revision, endpoint)
    download_disk_budget(root, spec[2], source_metadata=source_metadata)
    snapshot_download(repo_id=spec[1], revision=revision, local_dir=str(staging), allow_patterns=list(spec[3]),
                      max_workers=max(1, min(MAX_MODEL_DOWNLOAD_WORKERS, available_threads())))
    if not pinned_model_weights_valid(staging, spec[1], deep=True):
        raise RuntimeError("固定版本模型权重与程序内置可信 SHA-256 不符，拒绝执行不可信权重")
    if not source_metadata.get("authoritative"):
        print("当前使用内置权重哈希模式，配置文件来源无法独立证明，之后必须通过模型加载与实际生成验收", flush=True)
    if not verify_remote_file_hashes(staging, source_metadata):
        raise RuntimeError("模型权重和固定提交的远程 SHA 摘要不一致，已拒绝使用")
    if not folder_has_weights(staging):
        raise RuntimeError("模型文件未完整保存：" + spec[1])
    for item in staging.rglob("*.index.json"):
        weights = read_json(item, {}).get("weight_map")
        if not isinstance(weights, dict) or not weights or any(
                not (item.parent / part).is_file() for part in weights.values()):
            raise RuntimeError("模型缺少权重分片：" + str(item))
    manifest = model_files_manifest(staging)
    if not manifest:
        raise RuntimeError("模型下载结果为空：" + spec[1])
    atomic_json(staging / "download.json", {"repo": spec[1], "revision": revision, "endpoint": endpoint,
                                           "completed": now_stamp(), "complete": True,
                                           "files": manifest,
                                           "integrity": model_integrity_manifest(staging),
                                           "sha256": model_full_sha256_manifest(staging),
                                           "source_metadata": source_metadata})
    if not model_folder_complete(staging, spec, deep=True):
        raise RuntimeError("模型下载后的完整 SHA-256 校验未通过：" + spec[1])
    if target.exists():
        shutil.rmtree(target)
    staging.replace(target)


def download_native_worker(root, endpoint):
    configure_environment(root)
    os.environ["HF_ENDPOINT"] = endpoint
    os.environ["HF_HUB_OFFLINE"] = "0"
    from huggingface_hub import HfApi, snapshot_download
    target = model_path(root, VIDEO_MODEL_FOLDER)
    if native_video_folder_complete(target):
        return
    info = HfApi(endpoint="https://huggingface.co").model_info(
        repo_id=NATIVE_AUTO_REPO, files_metadata=True, timeout=SOURCE_METADATA_TIMEOUT)
    revision = str(info.sha)
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise RuntimeError("未能从官方仓库获取固定提交，已停止自动下载")
    metadata = official_model_metadata(NATIVE_AUTO_REPO, revision, endpoint)
    files = [item.rfilename for item in info.siblings if
             Path(item.rfilename).suffix.lower() in MODEL_DOWNLOAD_SECURITY_SUFFIXES]
    weights = [name for name in files if name.endswith(".safetensors")]
    if not weights or any(name not in metadata["hashes"] for name in weights):
        raise RuntimeError("原生模型权重没有完整的官方 SHA-256 校验数据")
    expected = sum(int(metadata["sizes"].get(name, 0)) for name in files)
    if expected < 2 * GB:
        raise RuntimeError("原生模型的远程文件大小异常，拒绝自动部署")
    free_disk = shutil.disk_usage(root).free
    if free_disk < NATIVE_AUTO_DISK_RESERVE + int(expected * DOWNLOAD_SPACE_MULTIPLIER):
        raise RuntimeError("自动视频模型至少需 %.1f GB 磁盘空间，当前剩余 %.1f GB" % (
            (NATIVE_AUTO_DISK_RESERVE + expected * DOWNLOAD_SPACE_MULTIPLIER) / GB, free_disk / GB))
    staging = target.with_name(target.name + ".downloading")
    staging.mkdir(parents=True, exist_ok=True)
    marker = read_json(staging / "download.json", {})
    if marker and marker.get("revision") != revision:
        shutil.rmtree(staging)
        staging.mkdir(parents=True, exist_ok=True)
    snapshot_download(repo_id=NATIVE_AUTO_REPO, revision=revision, local_dir=str(staging),
                      allow_patterns=files, max_workers=min(MAX_MODEL_DOWNLOAD_WORKERS, available_threads()),
                      endpoint=endpoint)
    if any(item.suffix.lower() == ".bin" for item in staging.rglob("*")):
        raise RuntimeError("原生模型自动下载出现不安全的 pickle 权重，已拒绝加载")
    if not native_component_layout_valid(staging):
        raise RuntimeError("原生模型缺少必要组件或权重分片")
    if not verify_remote_file_hashes(staging, metadata):
        raise RuntimeError("原生模型文件与官方提交 SHA 校验结果不符")
    manifest = model_files_manifest(staging)
    atomic_json(staging / "download.json", {
        "kind": "cogvideox", "complete": True, "repo": NATIVE_AUTO_REPO,
        "revision": revision, "files": manifest,
        "sha256": model_full_sha256_manifest(staging),
        "integrity": model_integrity_manifest(staging),
        "source_metadata": metadata, "completed": now_stamp()})
    if not native_video_folder_complete(staging, deep=True):
        raise RuntimeError("原生模型最终完整性验收失败")
    if target.exists():
        shutil.rmtree(target)
    staging.replace(target)


def download_voice_worker(root, endpoint):
    configure_environment(root)
    os.environ["HF_ENDPOINT"] = endpoint
    os.environ["HF_HUB_OFFLINE"] = "0"
    from huggingface_hub import hf_hub_download
    corrupt = voice_model_ready(root) and not voice_download_complete(root, deep=True)
    download_disk_budget(root, "voice")
    base = model_path(root, "voice")
    for file in (VOICE_FILE, VOICE_FILE + ".json"):
        hf_hub_download(repo_id=VOICE_REPO, filename=file, revision=VOICE_REVISION,
                        local_dir=str(base), force_download=corrupt)
    if not voice_model_ready(root):
        raise RuntimeError("中文离线语音模型缺失或配置无效")
    digest = hashlib.sha256()
    with voice_model_path(root).open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != VOICE_SHA256:
        raise RuntimeError("中文语音模型校验失败，请重试下载")
    atomic_json(base / "download.json", {"repo": VOICE_REPO, "revision": VOICE_REVISION,
                                         "completed": now_stamp(), "sha256": digest.hexdigest(),
                                         "endpoint": endpoint, "sample_hash": file_integrity_hash(voice_model_path(root))})


def piper_speak_worker(root, text_path, output):
    configure_environment(root)
    os.environ["HF_HUB_OFFLINE"] = "1"
    if not voice_download_complete(root):
        raise RuntimeError("中文离线语音模型或拼音资源不完整")
    from piper import PiperVoice
    text = Path(text_path).read_text(encoding="utf-8-sig").strip()
    if not text:
        raise RuntimeError("中文旁白文本为空")
    voice = PiperVoice.load(str(voice_model_path(root)), use_cuda=False)
    with wave.open(str(output), "wb") as writer:
        voice.synthesize_wav(text, writer)
    if audio_seconds(output) < .15:
        raise RuntimeError("中文离线语音未产生有效声音")


def piper_server_worker(root):
    configure_environment(root)
    os.environ["HF_HUB_OFFLINE"] = "1"
    if not voice_download_complete(root):
        raise RuntimeError("本地中文语音模型尚未验收")
    from piper import PiperVoice
    voice = PiperVoice.load(str(voice_model_path(root)), use_cuda=False)
    print("PIPER_RESPONSE:" + json.dumps({"ready": True}), flush=True)
    for line in sys.stdin:
        try:
            command = json.loads(line)
            if command.get("command") == "close":
                break
            input_path = Path(command["text_path"])
            output = Path(command["output"])
            text = input_path.read_text(encoding="utf-8-sig").strip()
            if not text:
                raise ValueError("旁白不能为空")
            output.parent.mkdir(parents=True, exist_ok=True)
            with wave.open(str(output), "wb") as writer:
                voice.synthesize_wav(text, writer)
            if audio_seconds(output) < .15:
                raise RuntimeError("语音合成未产生有效声音")
            data = {"ok": True, "output": str(output)}
        except Exception as error:
            data = {"ok": False, "error": str(error)[:500], "type": type(error).__name__}
        print("PIPER_RESPONSE:" + json.dumps(data, ensure_ascii=False), flush=True)


class PersistentPiper:
    def __init__(self, root, cancel, log):
        self.root = Path(root)
        self.cancel = cancel
        self.log = log
        self.responses = queue.Queue()
        self.finished = threading.Event()
        flags = (subprocess.CREATE_NO_WINDOW | 0x00004000) if os.name == "nt" else 0
        self.proc = subprocess.Popen([str(runtime_python(root)), "-u", str(Path(__file__).resolve()),
                                      "--speak-server", str(root)], cwd=str(root),
                                     env=shell_env(root, offline=True), stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                     encoding="utf-8", errors="replace", bufsize=1, creationflags=flags)
        with RUNNING_CHILDREN_LOCK:
            RUNNING_CHILDREN.add(self.proc)
        def reader():
            try:
                for line in self.proc.stdout:
                    if line.startswith("PIPER_RESPONSE:"):
                        try:
                            self.responses.put(json.loads(line[len("PIPER_RESPONSE:"):]))
                        except ValueError:
                            self.log("语音工作进程返回了无效数据")
                    elif line.strip():
                        self.log("语音引擎：" + line.strip()[:180])
            except (OSError, ValueError):
                pass
            finally:
                self.finished.set()
        self.reader = threading.Thread(target=reader, daemon=True)
        self.reader.start()
        try:
            ready = self._receive(90)
            if ready.get("ready") is not True:
                raise RuntimeError("常驻语音引擎未确认加载完成")
        except BaseException:
            self.close()
            raise

    def _receive(self, timeout):
        started = time.monotonic()
        while time.monotonic() - started < timeout:
            if self.cancel.is_set():
                raise InterruptedError("停止语音合成")
            if self.proc.poll() is not None and self.finished.is_set() and self.responses.empty():
                raise RuntimeError("语音工作进程意外退出：%s" % self.proc.returncode)
            try:
                message = self.responses.get(timeout=.2)
                if message.get("error"):
                    raise RuntimeError(str(message["error"]))
                return message
            except queue.Empty:
                continue
        raise TimeoutError("语音引擎响应超时")

    def synthesize(self, text_path, output):
        if self.proc.poll() is not None:
            raise RuntimeError("语音工作进程已经退出")
        data = {"text_path": str(text_path), "output": str(output)}
        self.proc.stdin.write(json.dumps(data, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        result = self._receive(MAX_SPEECH_RESPONSE_SECONDS)
        if not result.get("ok") or result.get("output") != str(output) or audio_seconds(output) < .15:
            raise RuntimeError("语音工作进程未正确产生 WAV 文件")
        return Path(output)

    def close(self):
        if self.proc.poll() is None:
            try:
                self.proc.stdin.write('{"command":"close"}\n')
                self.proc.stdin.flush()
                self.proc.wait(timeout=4)
            except (OSError, ValueError, subprocess.TimeoutExpired):
                stop_process_tree(self.proc)
        for stream in (self.proc.stdin, self.proc.stdout):
            if stream is not None:
                try:
                    stream.close()
                except OSError:
                    pass
        self.reader.join(timeout=2)
        with RUNNING_CHILDREN_LOCK:
            RUNNING_CHILDREN.discard(self.proc)

def check_runtime_worker(root, tier="full"):
    configure_environment(root)
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "DIFFUSERS_OFFLINE": "1"})
    import torch
    import imageio_ffmpeg
    import PIL
    import transformers
    import numpy as np
    from PIL import Image
    from transformers import (AutoTokenizer, AutoModelForCausalLM, WhisperProcessor,
                              WhisperForConditionalGeneration, CLIPProcessor, CLIPModel)
    torch.set_num_threads(available_threads())
    checks = {}
    def release():
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    folder = str(model_path(root, "director"))
    tokenizer = AutoTokenizer.from_pretrained(folder, local_files_only=True)
    director = AutoModelForCausalLM.from_pretrained(folder, torch_dtype=torch.float32,
                                                   local_files_only=True, low_cpu_mem_usage=True)
    director.eval()
    prompt = tokenizer("你好", return_tensors="pt")
    with torch.inference_mode():
        sample = director.generate(**prompt, max_new_tokens=2, do_sample=False,
                                   pad_token_id=tokenizer.eos_token_id)
    if sample.shape[1] <= prompt.input_ids.shape[1]:
        raise RuntimeError("本地文案模型未生成任何文字")
    checks["director"] = "passed"
    del tokenizer, director, prompt, sample
    release()
    if tier == "full":
        import diffusers
        import pypdf
        from diffusers import DiffusionPipeline
        folder = str(model_path(root, "listener"))
        listener_processor = WhisperProcessor.from_pretrained(folder, local_files_only=True)
        listener = WhisperForConditionalGeneration.from_pretrained(folder, local_files_only=True)
        listener.eval()
        batch = listener_processor(np.zeros(SPEECH_RATE, dtype=np.float32),
                                   sampling_rate=SPEECH_RATE, return_tensors="pt")
        with torch.inference_mode():
            ids = listener.generate(batch.input_features, max_new_tokens=4)
        if ids.numel() == 0:
            raise RuntimeError("本地语音识别模型没有产生结果")
        checks["listener"] = "passed"
        del listener_processor, listener, batch, ids
        release()
        folder = str(model_path(root, "inspector"))
        inspector_processor = CLIPProcessor.from_pretrained(folder, local_files_only=True, use_fast=False)
        inspector = CLIPModel.from_pretrained(folder, local_files_only=True, torch_dtype=torch.float32)
        inspector.eval()
        batch = inspector_processor(text=["a red square", "an empty background"],
                                    images=Image.new("RGB", (224, 224), "red"),
                                    return_tensors="pt", padding=True, truncation=True)
        with torch.inference_mode():
            logits = inspector(**batch).logits_per_image
        if logits.numel() != 2 or not torch.isfinite(logits).all():
            raise RuntimeError("画面审校模型输出不正确")
        checks["inspector"] = "passed"
        del inspector_processor, inspector, batch, logits
        release()
        painter = DiffusionPipeline.from_pretrained(str(model_path(root, "painter")),
                                                   torch_dtype=torch.float32, local_files_only=True,
                                                   low_cpu_mem_usage=True)
        painter.to("cpu")
        painter.set_progress_bar_config(disable=True)
        with torch.inference_mode():
            picture = painter("a red apple", width=256, height=256,
                              num_inference_steps=1, guidance_scale=1.0).images[0]
        if picture.width < 128 or picture.height < 128:
            raise RuntimeError("本地图像生成模型没有产生正确的画面")
        checks["painter"] = "passed"
        del painter, picture
        release()
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    temporary = Path(root) / ".studio" / "tmp" / "runtime_probe.mp4"
    try:
        result = subprocess.run([ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi",
                                 "-i", "color=c=red:s=160x160:r=8:d=1", "-f", "lavfi",
                                 "-i", "anullsrc=r=16000:cl=mono", "-t", "1", "-c:v", "libx264",
                                 "-pix_fmt", "yuv420p", "-c:a", "aac", str(temporary)],
                                capture_output=True, timeout=50,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        if result.returncode or not temporary.is_file() or temporary.stat().st_size < 2048:
            raise RuntimeError("视频和音频编码组件未通过实际输出测试：" + result.stderr.decode(errors="replace")[-400:])
    finally:
        temporary.unlink(missing_ok=True)
    checks["encoder"] = "passed"
    voice_backend = "sapi" if test_system_chinese_voice(root) else "piper"
    if voice_backend == "piper":
        voice_text = Path(root) / ".studio" / "tmp" / "voice_probe.txt"
        voice_wave = Path(root) / ".studio" / "tmp" / "voice_probe.wav"
        try:
            voice_text.write_text("你好，欢迎使用离线视频工坊。", encoding="utf-8-sig")
            piper_speak_worker(root, voice_text, voice_wave)
        finally:
            voice_text.unlink(missing_ok=True)
            voice_wave.unlink(missing_ok=True)
    checks["voice"] = "passed"
    print(json.dumps({"ok": True, "tier": tier, "smoke_test": checks, "chinese_voice": True,
                       "voice_backend": voice_backend,
                      "torch": torch.__version__, "cuda": torch.cuda.is_available(),
                      "ffmpeg": str(ffmpeg), "transformers": transformers.__version__,
                      "diffusers": diffusers.__version__ if tier == "full" else "not-installed",
                      "pillow": PIL.__version__}, ensure_ascii=False), flush=True)


def native_seam_positions(metadata):
    counts = metadata.get("frame_schedule", [])
    fps = metadata.get("fps", NATIVE_VIDEO_FPS)
    if not isinstance(counts, list) or not all(isinstance(count, int) and count >= 9 for count in counts):
        return []
    if not isinstance(fps, (int, float)) or not math.isfinite(fps) or fps <= 0:
        return []
    frames = counts[0] if counts else 0
    positions = []
    for count in counts[1:]:
        positions.append(((frames - 1) / fps, frames / fps))
        frames += count - 1
    if len(positions) > NATIVE_MAX_SEAM_SAMPLES:
        step = (len(positions) - 1) / max(1, NATIVE_MAX_SEAM_SAMPLES - 1)
        positions = [positions[round(index * step)] for index in range(NATIVE_MAX_SEAM_SAMPLES)]
    return positions


def image_mean_difference(first, second):
    from PIL import Image, ImageChops, ImageStat
    with Image.open(first) as left, Image.open(second) as right:
        a = left.convert("L").resize((96, 64))
        b = right.convert("L").resize((96, 64))
        return float(ImageStat.Stat(ImageChops.difference(a, b)).mean[0])


def extract_video_frame(ffmpeg, video, destination, seconds, root, cancel=None, log=None):
    run_external([str(ffmpeg), "-hide_banner", "-loglevel", "error", "-y", "-i", str(video),
                  "-ss", "%.6f" % max(0, float(seconds)), "-frames:v", "1", str(destination)],
                 root, cancel=cancel, log=log, timeout=110, capture=True)
    if not Path(destination).is_file():
        raise RuntimeError("指定时间点未能提取视频帧")
    return destination


def native_frame_schedule(seconds, fps=NATIVE_VIDEO_FPS, maximum=NATIVE_VIDEO_FRAMES):
    maximum = max(17, int(maximum) // 8 * 8 + 1)
    required = max(9, math.ceil(max(1.0, float(seconds)) * fps))
    segments = max(1, math.ceil((required - 1) / max(1, maximum - 1)))
    if segments > MAX_NATIVE_SEGMENTS:
        raise RuntimeError("当前安全分段上限无法覆盖 %.1f 秒连续动态视频" % float(seconds))
    remaining = required - 1
    counts = []
    for index in range(segments):
        addition = math.ceil(remaining / (segments - index))
        frames = min(maximum, max(9, math.ceil(addition / 8) * 8 + 1))
        counts.append(frames)
        remaining = max(0, remaining - (frames - 1))
    if remaining:
        raise RuntimeError("原生视频帧数规划不足，拒绝冻结末帧凑时长")
    return counts


def native_aspect_name(aspect):
    return "竖屏" if "竖屏" in str(aspect) else "方形" if "方形" in str(aspect) else "横屏"


def native_generation_resolution(aspect, free_bytes, model_class):
    if model_class not in {"CogVideoXPipeline", "CogVideoXImageToVideoPipeline"}:
        raise ValueError("当前原生视频模型类型不受支持")
    choices = NATIVE_RESOLUTIONS[native_aspect_name(aspect)]
    return choices[0] if free_bytes >= NATIVE_HIGH_MEMORY else choices[1 if len(choices) > 1 else 0]


def native_smaller_resolution(aspect, current, model_class):
    if model_class not in {"CogVideoXPipeline", "CogVideoXImageToVideoPipeline"}:
        raise ValueError("当前原生视频模型类型不受支持")
    choices = NATIVE_RESOLUTIONS[native_aspect_name(aspect)]
    old_area = int(current[0]) * int(current[1])
    for width, height in choices:
        if width * height < old_area and width <= current[0] and height <= current[1]:
            return width, height
    return None


def native_model_capabilities(pipeline, aspect, available_bytes, model_class):
    transformer = getattr(pipeline, "transformer", None)
    config = getattr(transformer, "config", None)
    scale = getattr(pipeline, "vae_scale_factor_spatial", 8)
    try:
        scale = max(1, min(32, int(scale)))
    except (TypeError, ValueError):
        scale = 8
    sample_width = getattr(config, "sample_width", None)
    sample_height = getattr(config, "sample_height", None)
    if isinstance(sample_width, int) and isinstance(sample_height, int) and sample_width > 0 and sample_height > 0:
        native_width, native_height = sample_width * scale, sample_height * scale
    else:
        native_width, native_height = native_generation_resolution(aspect, available_bytes, model_class)
    permitted = min(native_width * native_height, native_generation_resolution(aspect, available_bytes, model_class)[0] *
                    native_generation_resolution(aspect, available_bytes, model_class)[1])
    target = {"横屏": 16 / 9, "竖屏": 9 / 16, "方形": 1.0}[native_aspect_name(aspect)]
    width = max(16, int(math.sqrt(permitted * target) // 16 * 16))
    height = max(16, int(math.sqrt(permitted / target) // 16 * 16))
    width = min(width, max(16, native_width // 16 * 16))
    height = min(height, max(16, native_height // 16 * 16))
    width = max(16, width // 16 * 16)
    height = max(16, height // 16 * 16)
    reported_frames = getattr(config, "sample_frames", None)
    maximum = (min(NATIVE_VIDEO_MAX_FRAMES, reported_frames) if
               isinstance(reported_frames, int) and reported_frames >= 17 else
               NATIVE_VIDEO_MAX_FRAMES if available_bytes >= NATIVE_HIGH_MEMORY else NATIVE_VIDEO_FRAMES)
    maximum = max(17, int(maximum - 1) // 8 * 8 + 1)
    return {"resolution": (width, height), "frame_limit": maximum,
            "native_resolution": (native_width, native_height),
            "model_reported_frames": reported_frames}


def native_model_precision(torch, gpu_index):
    try:
        return torch.bfloat16 if torch.cuda.is_bf16_supported(including_emulation=False) else torch.float16
    except (AttributeError, RuntimeError, TypeError):
        try:
            capability = torch.cuda.get_device_capability(gpu_index)
            return torch.bfloat16 if capability[0] >= 8 else torch.float16
        except (AttributeError, RuntimeError, TypeError, ValueError):
            return torch.float16


def native_video_worker(root, prompt_path, output, quality, seconds=3.0, image_path=None, aspect="横屏 16:9"):
    configure_environment(root)
    os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "DIFFUSERS_OFFLINE": "1"})
    model = native_video_model(root)
    if model is None or not native_video_folder_complete(model[0], deep=True):
        raise RuntimeError("原生视频模型的完整 SHA-256 校验失败，请重新导入并离线加载验收")
    import torch
    from diffusers import CogVideoXPipeline, CogVideoXImageToVideoPipeline
    from diffusers.utils import export_to_video
    from PIL import Image, ImageOps
    if not torch.cuda.is_available():
        raise RuntimeError("原生视频需要 NVIDIA GPU；CPU 可使用图片动态运镜")
    if not native_inference_ready(root):
        raise RuntimeError("原生视频模型未通过真实推理和解码验收，已改用轻量动态运镜")
    verified_gpu = read_json(Path(root) / ".studio" / "native_ready.json", {})
    selected = select_torch_gpu(torch, NATIVE_VIDEO_MIN_FREE_MB * 1024 * 1024,
                                {"name": verified_gpu.get("gpu_name"),
                                 "total_mb": verified_gpu.get("gpu_total_mb"),
                                 "index": verified_gpu.get("gpu_index")})
    if not selected:
        raise RuntimeError("当前已验证的 GPU 显存不足或不再可见，请重新验收")
    free, total, gpu_index = selected["free_bytes"], selected["total_bytes"], selected["index"]
    torch.cuda.set_device(gpu_index)
    prompt = Path(prompt_path).read_text(encoding="utf-8").strip()
    image_mode = model[1] == "CogVideoXImageToVideoPipeline"
    if image_mode and (not image_path or not Path(image_path).is_file()):
        raise RuntimeError("当前图生视频模型需要可读取的参考图片")
    cls = CogVideoXImageToVideoPipeline if image_mode else CogVideoXPipeline
    steps = NATIVE_VIDEO_STEPS.get(quality, NATIVE_VIDEO_STEPS["智能"])
    precision = native_model_precision(torch, gpu_index)
    pipeline = cls.from_pretrained(str(model[0]), local_files_only=True, torch_dtype=precision)
    limits = native_model_capabilities(pipeline, aspect, free, model[1])
    schedule = native_frame_schedule(seconds, maximum=limits["frame_limit"])
    if not image_mode and len(schedule) > 1:
        del pipeline
        raise RuntimeError("当前文生视频模型无法保证长片段跨段一致性；请改用图生视频模型或分镜图片运镜")
    original_resolution = limits["resolution"]
    pipeline.enable_model_cpu_offload(gpu_id=gpu_index)
    if hasattr(pipeline, "vae") and hasattr(pipeline.vae, "enable_tiling"):
        pipeline.vae.enable_tiling()
    reference = None
    if image_mode:
        with Image.open(image_path) as original:
            reference = ImageOps.exif_transpose(original).convert("RGB")
    segments = []
    width, height = original_resolution
    try:
        for number, count in enumerate(schedule):
            generated = None
            params = {"prompt": prompt[:600], "num_frames": count,
                      "num_inference_steps": steps, "guidance_scale": 6.0,
                      "height": height, "width": width}
            if image_mode:
                params["image"] = ImageOps.pad(reference, (width, height), method=Image.Resampling.LANCZOS,
                                               color=(12, 12, 12))
            try:
                with torch.inference_mode():
                    generated = pipeline(**params).frames[0]
            except (RuntimeError, MemoryError) as error:
                smaller = native_smaller_resolution(aspect, (width, height), model[1])
                if number != 0 or not is_memory_error(error) or smaller is None:
                    raise
                torch.cuda.empty_cache()
                width, height = smaller
                params.update({"height": height, "width": width,
                               "num_inference_steps": min(steps, NATIVE_VIDEO_STEPS["快速"])})
                if image_mode:
                    params["image"] = ImageOps.pad(reference, (width, height), method=Image.Resampling.LANCZOS,
                                                   color=(12, 12, 12))
                print("显存不足，已按原画幅缩小到 %d×%d 后重试" % (width, height), flush=True)
                with torch.inference_mode():
                    generated = pipeline(**params).frames[0]
            if not generated or len(generated) < 9:
                raise RuntimeError("原生视频第 %d 段未生成有效连续帧" % (number + 1))
            if image_mode:
                reference = generated[-1].convert("RGB")
            if number:
                generated = generated[1:]
            segment = Path(output).with_name(Path(output).stem + "_part_%02d.mp4" % number)
            export_to_video(generated, str(segment), fps=NATIVE_VIDEO_FPS)
            if not segment.is_file() or segment.stat().st_size < 8192:
                raise RuntimeError("原生视频第 %d 段编码失败" % (number + 1))
            segments.append(segment)
            print("原生动态片段 %d/%d 完成，真实帧数 %d" % (number + 1, len(schedule), len(generated)), flush=True)
            del generated
            gc.collect()
            torch.cuda.empty_cache()
        concat_file = Path(output).with_name(Path(output).stem + "_parts.txt")
        concat_file.write_text("\n".join("file '%s'" % str(part).replace("\\", "/").replace("'", "'\\''")
                                         for part in segments), encoding="utf-8")
        result = run_external([ffmpeg_executable(), "-hide_banner", "-loglevel", "error", "-y",
                               "-f", "concat", "-safe", "0", "-i", str(concat_file),
                               "-t", "%.4f" % (max(float(seconds), 1.0) + 2 / NATIVE_VIDEO_FPS),
                               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(NATIVE_VIDEO_FPS),
                               "-an", str(output)], root, timeout=max(360, int(seconds * 60)),
                              env=shell_env(root, offline=True), capture=True)
        if not Path(output).is_file() or Path(output).stat().st_size < 8192:
            raise RuntimeError("原生视频合成没有产生有效视频")
        full_frames = sum(schedule) - (len(schedule) - 1)
        actual_seconds = full_frames / NATIVE_VIDEO_FPS
        if actual_seconds < float(seconds) / MAX_NATIVE_OUTPUT_DURATION_FACTOR:
            raise RuntimeError("动态片段合计时长不足，禁止使用冻结末帧补齐")
        atomic_json(str(output) + ".json", {"frames": full_frames, "fps": NATIVE_VIDEO_FPS,
                    "seconds": round(actual_seconds, 4), "requested_seconds": float(seconds),
                    "segments": len(schedule), "frame_schedule": schedule,
                    "model_class": model[1], "reference_signature": file_integrity_hash(image_path) if image_path else None,
                    "resolution": [width, height], "model_native_resolution": list(limits["native_resolution"]),
                    "model_reported_frames": limits["model_reported_frames"],
                    "precision": str(precision), "aspect": aspect, "generated": now_stamp(),
                    "motion_fill": "image_conditioned_continuations" if image_mode else "single_t2v_sequence"})
    finally:
        del pipeline
        gc.collect()
        torch.cuda.empty_cache()


def test_system_chinese_voice(root):
    if os.name != "nt":
        return False
    script = Path(root) / ".studio" / "tmp" / "check_voice.ps1"
    sample = Path(root) / ".studio" / "tmp" / "check_voice.wav"
    outfile = str(sample).replace("'", "''")
    script.write_text("Add-Type -AssemblyName System.Speech\n"
                      "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
                      "$c=@($s.GetInstalledVoices() | Where-Object { $_.VoiceInfo.Culture.Name -like 'zh*' -and $_.Enabled })\n"
                      "if ($c.Count -eq 0) { throw 'CHINESE_VOICE_MISSING' }\n"
                      "$s.SelectVoice($c[0].VoiceInfo.Name)\n"
                      "$s.SetOutputToWaveFile('" + outfile + "')\n"
                      "$s.Speak('你好')\n"
                      "$s.Dispose()\n", encoding="utf-8-sig")
    try:
        result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy",
                                 "Bypass", "-File", str(script)], capture_output=True, timeout=30,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        return result.returncode == 0 and sample.is_file() and sample.stat().st_size > 1000
    except (OSError, subprocess.TimeoutExpired):
        return False
    finally:
        script.unlink(missing_ok=True)
        sample.unlink(missing_ok=True)


def voice_backend_operational(root, backend, force=False):
    if backend == "piper":
        return voice_download_complete(root, deep=force)
    if backend != "sapi" or os.name != "nt":
        return False
    key = str(Path(root).resolve())
    with VOICE_PROBE_LOCK:
        prior = VOICE_PROBE_CACHE.get(key, {})
        if (prior and time.monotonic() - prior["at"] < VOICE_PROBE_SECONDS and
                (not force or prior.get("deep"))):
            return bool(prior["ok"])
        try:
            if force:
                healthy = test_system_chinese_voice(root)
            else:
                command = ("Add-Type -AssemblyName System.Speech;"
                           "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
                           "$v=@($s.GetInstalledVoices() | Where-Object {"
                           "$_.Enabled -and $_.VoiceInfo.Culture.Name -like 'zh*'});"
                           "if($v.Count -lt 1){exit 2};$s.Dispose()")
                result = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive",
                                         "-ExecutionPolicy", "Bypass", "-Command", command],
                                        capture_output=True, timeout=12,
                                        creationflags=subprocess.CREATE_NO_WINDOW)
                healthy = result.returncode == 0
        except (OSError, ValueError, subprocess.TimeoutExpired):
            healthy = False
        VOICE_PROBE_CACHE[key] = {"at": time.monotonic(), "ok": healthy, "deep": bool(force)}
        return healthy


def ffmpeg_executable():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def asset_sequence_for_scene(primary, extras, index, count, request):
    extras = list(extras or [])
    sequence = ([primary] if primary else []) + extras
    if primary and index == count - 1 and request.get("files", {}).get("尾帧"):
        sequence = extras + [primary]
    if not sequence:
        return []
    return sequence


def distribute_unused_assets(scenes, assignments, unused, request, seconds, fps=DEFAULT_FPS):
    count = len(scenes)
    extras = {index: [] for index in range(count)}
    frames = [max(1, round(float(seconds[index]) * fps)) for index in range(count)]
    minimum = max(3, math.ceil(MIN_ASSET_SHOT_SECONDS * fps))
    remaining = []
    for item in unused:
        possibilities = [index for index in range(count)
                         if (len(extras[index]) + (1 if index in assignments else 0) < MAX_ASSETS_PER_SCENE and
                             (len(extras[index]) + (2 if index in assignments else 1)) * minimum <= frames[index])]
        if not possibilities:
            remaining.append(item)
            continue
        place = min(possibilities, key=lambda index: (
            (len(extras[index]) + (1 if index in assignments else 0)) / max(1, frames[index]),
            len(extras[index]), index))
        extras[place].append(item)
    if remaining:
        raise RuntimeError("所选素材超过当前成片的可观看时长，仍有 %d 个未能安排。请增加时长或减少素材，程序不会悄悄丢弃" % len(remaining))
    return {index: items for index, items in extras.items() if items}


def montage_frame_allocation(seconds, items, fps):
    count = len(items)
    if count <= 0:
        raise ValueError("镜头素材为空")
    total = round(float(seconds) * fps)
    minimum = max(3, math.ceil(MIN_ASSET_SHOT_SECONDS * fps))
    if count * minimum > total:
        raise RuntimeError("当前镜头 %.2f 秒不足以完整展示 %d 个素材，建议增加片长" % (seconds, count))
    base = max(minimum, total // count)
    counts = [base] * count
    remain = total - sum(counts)
    for index in range(remain):
        counts[index % count] += 1
    if sum(counts) != total:
        raise RuntimeError("素材编排帧数不一致")
    return [number / fps for number in counts]


def repair_action_for(code):
    if code in {"SPEECH_REVIEW_UNAVAILABLE", "SEMANTIC_REVIEW_UNAVAILABLE",
                "TEMPORAL_REVIEW_UNAVAILABLE"}:
        return "restart_reviewer_and_recheck"
    if code == "CAPTION_TIMELINE_MISSING":
        return "rebuild_timeline"
    if code in {"MIXED_VOICE_MISSING", "MIXED_SPEECH_MISMATCH", "MIXED_AUDIO_EXTRACTION_FAILED"}:
        return "remix_audio"
    if code in {"CAPTION_VISIBILITY", "CAPTION_TIMELINE_MISMATCH", "SPEECH_MISMATCH",
                "SPEECH_SOURCE_MISMATCH", "SPEECH_SOURCE_MISSING"}:
        return "reencode_caption_keep_visual"
    if code == "TEMPORAL_FLICKER":
        return "disable_synthetic_motion_keep_visual"
    if code in {"AUDIO_LOW", "AUDIO_SCAN_FAILED", "OUTPUT_MISSING"}:
        return "repair_audio_or_container"
    if code in {"SCENE_FRAME_INVALID", "FINAL_SEMANTIC_MISMATCH"}:
        return "repair_scene_visual"
    return "reencode_final_container"


def image_font(size):
    from PIL import ImageFont
    fonts = [Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts" / name for name in
             ("msyh.ttc", "msyhbd.ttc", "simhei.ttf", "simsun.ttc", "arial.ttf")]
    fonts.extend([Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"), Path("/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc")])
    for path in fonts:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_text(text, font, width, max_lines=None, truncate=False):
    lines = []
    for paragraph in re.split(r"[\r\n]+", str(text)):
        tokens = re.findall(r"[A-Za-z0-9]+|[^A-Za-z0-9\s]|\s+", paragraph)
        current = ""
        for token in tokens:
            if not current and not token.strip():
                continue
            if font.getlength(current + token) <= width:
                current += token
                continue
            if current.strip():
                lines.append(current.rstrip())
                current = ""
            if token.strip():
                if font.getlength(token) <= width:
                    current = token
                else:
                    for char in token:
                        if current and font.getlength(current + char) > width:
                            lines.append(current.rstrip())
                            current = ""
                        current += char
        if current.strip():
            lines.append(current.rstrip())
    if max_lines is not None and len(lines) > max_lines:
        if not truncate:
            raise ValueError("字幕需要分页显示，不允许隐藏正文")
        lines = lines[:max_lines]
        tail = lines[-1]
        while tail and font.getlength(tail + "…") > width:
            tail = tail[:-1]
        lines[-1] = tail + "…"
    return lines


def normalized_caption(value):
    return re.sub(r"\s+", "", str(value))


def paginate_caption(caption, size, seconds, fps=DEFAULT_FPS):
    text = str(caption).strip()
    if not text:
        return []
    font = image_font(max(MIN_CAPTION_FONT, int(size[1] * .044)))
    lines = wrap_text(text, font, int(size[0] * CAPTION_MAX_WIDTH_FRACTION))
    pages = ["\n".join(lines[i:i + MAX_CAPTION_LINES])
             for i in range(0, len(lines), MAX_CAPTION_LINES)]
    if not pages or len(pages) > MAX_CAPTION_SEGMENTS:
        raise ValueError("旁白太长，无法在单镜头中完整显示，请缩短文案或增加镜头数量")
    if normalized_caption("".join(pages)) != normalized_caption(text):
        raise ValueError("分段字幕文本未能完整覆盖原始旁白")
    frames = round(float(seconds) * fps)
    minimum = max(3, round(.2 * fps))
    if frames < minimum * len(pages):
        raise ValueError("字幕过密，当前镜头时长无法完整呈现全部文字")
    weights = [max(1, narration_units(part)) for part in pages]
    remaining = frames - minimum * len(pages)
    exact = [remaining * weight / sum(weights) for weight in weights]
    extras = [int(value) for value in exact]
    for index in sorted(range(len(extras)), key=lambda i: exact[i] - extras[i], reverse=True)[:remaining - sum(extras)]:
        extras[index] += 1
    cursor = 0
    result = []
    for page, extra in zip(pages, extras):
        following = cursor + minimum + extra
        result.append({"text": page, "start": round(cursor / fps, 6), "end": round(following / fps, 6)})
        cursor = following
    return result


def frame_with_caption(source, output, size, caption, title="", transparent=False):
    from PIL import Image, ImageDraw, ImageFilter, ImageOps
    width, height = size
    if transparent:
        canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    else:
        with Image.open(source) as original:
            original.draft("RGB", (width * 2, height * 2))
            original.thumbnail((width * 2, height * 2), Image.Resampling.LANCZOS)
            image = ImageOps.exif_transpose(original).convert("RGB")
        backdrop = ImageOps.fit(image, size, method=Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(max(3, width // 100)))
        foreground = ImageOps.contain(image, size, method=Image.Resampling.LANCZOS)
        backdrop.paste(foreground, ((width - foreground.width) // 2, (height - foreground.height) // 2))
        canvas = backdrop.convert("RGBA")
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    text = str(caption or "").strip()
    scale = max(MIN_CAPTION_FONT, int(height * .044))
    font = image_font(scale)
    lines = wrap_text(text, font, int(width * CAPTION_MAX_WIDTH_FRACTION), MAX_CAPTION_LINES)
    row = int(scale * 1.4)
    pad = max(10, int(height * .025))
    block_height = len(lines) * row + 2 * pad
    top = height - block_height - int(height * .045)
    if lines:
        draw.rounded_rectangle((int(width * .035), top, int(width * .965), top + block_height), radius=pad,
                               fill=(0, 0, 0, 170))
        for index, line in enumerate(lines):
            left = int((width - font.getlength(line)) / 2)
            draw.text((left, top + pad + index * row), line, font=font, fill=(250, 250, 252, 255), stroke_width=0)
    if title:
        label_font = image_font(max(14, int(height * .032)))
        short = wrap_text(title, label_font, int(width * .85), 1, truncate=True)
        if short:
            tw = int(label_font.getlength(short[0]))
            draw.rounded_rectangle((int(width * .04), int(height * .04), int(width * .04) + tw + 2 * pad,
                                    int(height * .04) + int(label_font.size * 1.6)), radius=pad // 2,
                                   fill=(0, 0, 0, 125))
            draw.text((int(width * .04) + pad, int(height * .045)), short[0], font=label_font, fill="white")
    result = Image.alpha_composite(canvas, layer)
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    result.save(output)
    return output


def validate_image(path, allow_flat=False):
    from PIL import Image, ImageStat
    try:
        with Image.open(path) as picture:
            picture.verify()
        with Image.open(path) as picture:
            if min(picture.size) < 128:
                return False, "尺寸过小"
            picture.draft("RGB", (256, 256))
            picture.thumbnail((256, 256))
            gray = picture.convert("L").resize((128, 128))
            spread = ImageStat.Stat(gray).stddev[0]
            if spread < 8 and not allow_flat:
                return False, "内容过于单调"
        return True, "通过"
    except (OSError, ValueError) as error:
        return False, str(error)


def caption_visible(reference, actual):
    from PIL import Image, ImageOps
    with Image.open(reference) as template, Image.open(actual) as frame:
        reference_image = template.convert("RGBA")
        picture = ImageOps.fit(frame.convert("RGB"), reference_image.size)
        width, height = reference_image.size
        region = (0, int(height * .55), width, height)
        candidate = reference_image.crop(region)
        observed = picture.crop(region)
        source = candidate.getdata()
        dest = observed.getdata()
        meaningful = matched = 0
        glyph_brightness = panel_brightness = panel_pixels = 0
        for rgba, rgb in zip(source, dest):
            brightness = sum(rgb) / 3
            if rgba[3] > 235 and min(rgba[:3]) > 225:
                meaningful += 1
                glyph_brightness += brightness
                if min(rgb) >= 145:
                    matched += 1
            elif 100 <= rgba[3] <= 230 and max(rgba[:3]) <= 45:
                panel_pixels += 1
                panel_brightness += brightness
        threshold = max(18, width * height // 16000)
        contrast = ((glyph_brightness / meaningful) - (panel_brightness / panel_pixels)
                    if meaningful and panel_pixels else 0)
        readable = (meaningful >= threshold and panel_pixels >= threshold * 2
                    and matched / meaningful >= .7 and contrast >= 38)
        return readable, {"white_text_pixels": meaningful,
                          "visible_ratio": round(matched / meaningful, 3) if meaningful else 0,
                          "text_panel_contrast": round(contrast, 2), "panel_pixels": panel_pixels}


def extract_json_object(text):
    begin = str(text).find("{")
    if begin < 0:
        return None
    level = 0
    quoted = False
    escaped = False
    for position in range(begin, len(text)):
        char = text[position]
        if escaped:
            escaped = False
        elif char == "\\" and quoted:
            escaped = True
        elif char == '"':
            quoted = not quoted
        elif not quoted:
            if char == "{":
                level += 1
            elif char == "}":
                level -= 1
                if level == 0:
                    try:
                        return json.loads(text[begin:position + 1])
                    except ValueError:
                        return None
    return None


def validate_plan(plan, count):
    if not isinstance(plan, dict) or not isinstance(plan.get("scenes"), list):
        return False
    scenes = plan["scenes"]
    if len(scenes) != count:
        return False
    if not all(isinstance(scene, dict) and isinstance(scene.get("visual_prompt"), str)
               and len(scene["visual_prompt"].strip()) >= 10
               and isinstance(scene.get("narration"), str)
               and len(scene["narration"].strip()) >= 3 for scene in scenes):
        return False
    return True


def review_failure_type(review):
    if not isinstance(review, dict):
        return "generation_failed"
    if review.get("temporal_review_passed") is False:
        return "motion_insufficient"
    if review.get("technical_passed") is False:
        return "invalid_media"
    if float(review.get("cosine") or 0) < float(review.get("required_cosine", MIN_CLIP_COSINE)):
        return "subject_mismatch"
    if float(review.get("margin") if review.get("margin") is not None else -1) < float(
            review.get("required_margin", MIN_CLIP_MARGIN)):
        return "semantic_ambiguous"
    return "composition_or_continuity"


def visual_constraints(text):
    text = str(text)
    colors = {"红色": "red", "蓝色": "blue", "绿色": "green", "黄色": "yellow", "黑色": "black",
              "白色": "white", "紫色": "purple", "粉色": "pink", "金色": "gold", "银色": "silver"}
    descriptions = [value for key, value in colors.items() if key in text]
    for word in ("red", "blue", "green", "yellow", "black", "white", "purple", "pink", "gold", "silver"):
        if re.search(r"\b" + word + r"\b", text, re.I):
            descriptions.append(word)
    descriptions += re.findall(r"(?<![A-Za-z0-9])\d+(?:\.\d+)?(?:\s*[%％]|\s*个|\s*只|\s*人|\s*辆)?", text)[:12]
    digits = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6,
              "七": 7, "八": 8, "九": 9, "十": 10}
    units = {"个": "objects", "只": "objects", "人": "people", "位": "people", "辆": "vehicles",
             "台": "units", "棵": "trees", "朵": "flowers", "把": "objects", "条": "objects",
             "头": "animals", "匹": "animals", "枚": "objects", "架": "vehicles", "张": "objects"}
    for match in re.finditer(r"([一二两三四五六七八九十]{1,3})(个|只|人|位|辆|台|棵|朵|把|条|头|匹|枚|架|张)", text):
        token, unit = match.groups()
        if "十" in token:
            left, _, right = token.partition("十")
            count = (digits.get(left, 1) if left else 1) * 10 + (digits.get(right, 0) if right else 0)
        else:
            count = digits.get(token, 0)
        if count:
            descriptions.append("%d %s" % (count, units[unit]))
    return list(dict.fromkeys(descriptions))


def visual_constraints_retained(text, anchors):
    normalized = " " + re.sub(r"\s+", " ", str(text).lower()) + " "
    names = {"objects": "objects?|items?|things?", "people": "persons?|people|humans?",
             "vehicles": "vehicles?|cars?|trucks?|buses?|vans?", "units": "units?|devices?",
             "trees": "trees?", "flowers": "flowers?", "animals": "animals?|dogs?|cats?|horses?"}
    count_words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
                   7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    for anchor in anchors:
        parts = re.fullmatch(r"([0-9]+) ([a-z]+)", anchor)
        if parts:
            number, kind = parts.groups()
            digits = r"\b(?:" + re.escape(number) + "|" + count_words.get(int(number), number) + r")\b"
            if not re.search(digits, normalized) or not re.search(r"\b(?:" + names.get(kind, kind) + r")\b", normalized):
                return False
        elif not re.search(r"\b" + re.escape(anchor) + r"\b", normalized, re.I):
            return False
    return True


def refine_visual_prompt(prompt, review, attempt, user_constraints=""):
    original = re.sub(r"\s+", " ", str(prompt)).strip()[:360]
    corrections = {
        "generation_failed": "Use a simple, recognizable scene with stable geometry and clear subject boundaries.",
        "invalid_media": "Avoid artifacts, invalid textures and incoherent shapes; keep a fully visible subject.",
        "subject_mismatch": "Make the exact subject and requested attributes visually unmistakable.",
        "semantic_ambiguous": "Emphasize the original scene rather than a generic landscape or unrelated symbols.",
        "motion_insufficient": "Visible progression and changing physical positions, not a still image.",
        "composition_or_continuity": "Preserve scene identity with natural perspective and consistent lighting."
    }
    cause = review_failure_type(review)
    anchors = visual_constraints(user_constraints + " " + original)
    keep = (" Keep these explicit attributes unchanged: " + ", ".join(anchors[:12]) + ".") if anchors else ""
    return (original + " " + corrections[cause] + keep +
            " Keep all explicitly requested subjects, quantities and colors unchanged.")[:610]


def visual_review_record(technical_passed, semantic=None, constraint_passed=True,
                         supplied=False, reason=""):
    semantic_ok = semantic.get("passed") if isinstance(semantic, dict) else None
    state = ("invalid" if not technical_passed else "constraint_failed" if not constraint_passed else
             "unreviewed" if semantic_ok is None else "accepted" if semantic_ok else
             "supplied_conflict" if supplied else "rejected")
    return {"technical_passed": bool(technical_passed), "semantic_passed": semantic_ok,
            "constraints_passed": bool(constraint_passed),
            "overall_passed": bool(technical_passed and constraint_passed and semantic_ok is True),
            "review_status": state, "failure_type": review_failure_type(semantic) if semantic_ok is False else "",
            "reason": str(reason)[:200], "user_supplied": bool(supplied),
            "passed": bool(technical_passed and constraint_passed and semantic_ok is True)}


def normalize_spoken_text(value):
    return "".join(re.findall(r"[\u3400-\u9fffA-Za-z0-9]+", str(value).lower()))


def voice_presence_correlation(original, mixed, limit_seconds=MAX_VOICE_CORRELATION_SECONDS):
    import numpy as np
    arrays = []
    for path in (original, mixed):
        with wave.open(str(path), "rb") as stream:
            if (stream.getnchannels() != 1 or stream.getsampwidth() != 2 or
                    stream.getframerate() != SPEECH_RATE):
                raise ValueError("语音相关性检查需要 16 kHz 单声道 PCM")
            raw = stream.readframes(int(limit_seconds * SPEECH_RATE))
        arrays.append(np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0)
    first, second = arrays
    count = min(len(first), len(second))
    if count < SPEECH_RATE // 3:
        return 0.0
    first = first[:count].astype(np.float64)
    second = second[:count].astype(np.float64)
    first -= first.mean()
    second -= second.mean()
    denominator = math.sqrt(float(np.dot(first, first)) * float(np.dot(second, second)))
    if denominator < 1e-7:
        return 0.0
    length = 1 << (2 * count - 1).bit_length()
    cross = np.fft.irfft(np.fft.rfft(second, n=length) *
                         np.conj(np.fft.rfft(first, n=length)), n=length)
    shift = min(int(MAX_VOICE_ALIGNMENT_SECONDS * SPEECH_RATE), count // 4)
    values = np.concatenate((cross[-shift:], cross[:shift + 1]))
    return max(0.0, min(1.0, float(np.max(values)) / denominator))


def speech_review_failure(review):
    if review.get("status") == "missing_voice":
        return "SPEECH_SOURCE_MISSING"
    if review.get("status") == "mix_extract_failed":
        return "MIXED_AUDIO_EXTRACTION_FAILED"
    if review.get("status") == "recognition_unavailable":
        return "SPEECH_REVIEW_UNAVAILABLE"
    if review.get("status") == "mix_voice_missing":
        return "MIXED_VOICE_MISSING"
    original = review.get("source", {})
    mixed = review.get("mixed", {})
    if (original.get("status") == "suspected_mismatch" and
            original.get("observed_length", 0) >= MIN_SPEECH_REVIEW_CHARS):
        return "SPEECH_SOURCE_MISMATCH"
    if mixed.get("status") == "suspected_mismatch" and (
            mixed.get("observed_length", 0) >= MIN_SPEECH_REVIEW_CHARS or
            original.get("status") == "matched"):
        return "MIXED_SPEECH_MISMATCH"
    if (mixed.get("observed_length", 0) == 0 and original.get("status") == "matched" and
            original.get("expected_length", 0) >= MIN_SPEECH_REVIEW_CHARS):
        return "MIXED_SPEECH_MISMATCH"
    return None


def speech_match(expected, observed):
    expected_text = normalize_spoken_text(expected)
    observed_text = normalize_spoken_text(re.sub(r"\[\d+秒\]", " ", str(observed)))
    if not expected_text:
        return {"score": 1.0, "status": "empty_expected", "expected_length": 0, "observed_length": len(observed_text)}
    score = difflib.SequenceMatcher(None, expected_text, observed_text, autojunk=False).ratio()
    status = ("not_confident" if len(expected_text) < MIN_SPEECH_REVIEW_CHARS else
              "suspected_mismatch" if score < MIN_SPEECH_SIMILARITY else
              "needs_manual_check" if score < .72 else "matched")
    return {"score": round(score, 4), "status": status,
            "expected_length": len(expected_text), "observed_length": len(observed_text),
            "observed_excerpt": observed_text[:90]}


def fallback_plan(prompt, count, seconds):
    trimmed = re.sub(r"\s+", " ", prompt).strip()[:220]
    phrases = [part.strip() for part in re.split(r"[。！？；;，,\n]+", trimmed) if part.strip()]
    if not phrases:
        phrases = ["用户指定的主题"]
    stages = ("交代核心主题", "展现重要细节", "推进关键内容", "呈现不同视角", "强化重点信息", "收束主题与情绪")
    views = ("wide establishing shot", "medium narrative shot", "detailed close-up", "side angle",
             "cinematic perspective", "gentle concluding shot")
    scenes = []
    for i in range(count):
        index = min(len(stages) - 1, int(i * len(stages) / count))
        focus = phrases[i % len(phrases)]
        introduction = ("开场先看" if i == 0 else "最后回到" if i == count - 1 else "接着呈现")
        narration = short_narration(introduction + focus, 30)
        visual = ("A coherent cinematic %s illustrating: %s. Consistent subject identity, realistic details, "
                  "natural lighting, purposeful composition" % (views[index], focus))
        scenes.append({"narration": narration, "visual_prompt": visual[:330],
                       "seconds": round(seconds / count, 2)})
    return {"title": trimmed[:36] or "AI 创作", "mood": "inspiring", "scenes": scenes}


def normalize_plan(proposed, prompt, count, seconds):
    fallback = fallback_plan(prompt, count, seconds)
    if not isinstance(proposed, dict):
        return fallback
    given = proposed.get("scenes")
    if not isinstance(given, list):
        given = []
    scenes = []
    for index in range(count):
        entry = given[index] if index < len(given) and isinstance(given[index], dict) else {}
        baseline = fallback["scenes"][index]
        narration = str(entry.get("narration", "")).strip()
        visual = str(entry.get("visual_prompt", "")).strip()
        scenes.append({"narration": narration[:130] if narration_units(narration) >= 3 else baseline["narration"],
                       "visual_prompt": visual[:340] if len(visual) >= 10 else baseline["visual_prompt"],
                       "seconds": baseline["seconds"]})
    mood = str(proposed.get("mood", "inspiring"))
    if mood not in {"warm", "calm", "mysterious", "energetic", "inspiring"}:
        mood = "inspiring"
    title = str(proposed.get("title") or fallback["title"]).strip()[:45]
    return {"title": title, "mood": mood, "scenes": scenes}

def pdf_ocr_text(path, pages=None):
    import numpy as np
    import pypdfium2
    from rapidocr import RapidOCR
    engine = RapidOCR()
    document = pypdfium2.PdfDocument(str(path))
    count = len(document)
    targets = pages if pages is not None else range(min(count, OCR_PAGES))
    pieces = []
    total = 0
    try:
        for index in targets:
            if index < 0 or index >= count or total >= MAX_DOCUMENT_TEXT:
                break
            page = document[index]
            image = page.render(scale=OCR_PAGE_SCALE).to_pil().convert("RGB")
            if image.width * image.height > 6 * 1024 * 1024:
                image.thumbnail((2400, 2400))
            answer = engine(np.asarray(image))
            lines = [str(item).strip() for item in (getattr(answer, "txts", None) or []) if str(item).strip()]
            text = " ".join(lines)[:MAX_DOCUMENT_TEXT - total]
            if text:
                pieces.append("[扫描页 %d] %s" % (index + 1, text))
                total += len(text)
            page.close()
    finally:
        document.close()
    return "\n".join(pieces)[:MAX_DOCUMENT_TEXT]


def document_text(path):
    path = Path(path)
    extension = path.suffix.lower()
    size = path.stat().st_size
    if size > MAX_DOCUMENT_BYTES:
        raise ValueError("文档超过可安全解析的大小上限（%d MB）" % (MAX_DOCUMENT_BYTES // (1024 * 1024)))
    if extension in {".txt", ".md", ".csv", ".json", ".srt"}:
        with path.open("rb") as handle:
            contents = handle.read(min(size, MAX_DOCUMENT_BYTES))
        if contents.startswith((b"\xff\xfe", b"\xfe\xff")):
            encodings = ("utf-16", "utf-8-sig", "gb18030")
        elif contents[:128].count(b"\x00") > 12:
            odd_nulls = contents[1:128:2].count(0)
            even_nulls = contents[0:128:2].count(0)
            encodings = (("utf-16-le" if odd_nulls > even_nulls else "utf-16-be"), "utf-8-sig", "gb18030")
        else:
            encodings = ("utf-8-sig", "gb18030")
            try:
                utf8_text = contents[:2048].decode("utf-8-sig")
                utf8_error = None
            except UnicodeDecodeError as error:
                utf8_text = ""
                utf8_error = error
            unusual_controls = sum(ord(char) < 32 and char not in "\n\r\t" for char in utf8_text)
            suspicious_utf8 = bool(utf8_text and unusual_controls > max(2, len(utf8_text) // 80))
            if suspicious_utf8 or (utf8_error is not None and not (
                    utf8_error.reason == "unexpected end of data" and utf8_error.start >= len(contents) - 4)):
                ratings = []
                for candidate in ("utf-16-le", "utf-16-be"):
                    try:
                        sample = contents[:2048].decode(candidate)
                    except UnicodeDecodeError:
                        continue
                    meaningful = sum("\u3400" <= char <= "\u9fff" for char in sample)
                    controls = sum(ord(char) < 32 and char not in "\n\r\t" for char in sample)
                    if len(sample) >= 8 and controls == 0:
                        ratings.append((meaningful / len(sample), candidate))
                ratings.sort(reverse=True)
                if ratings and ratings[0][0] > .7 and (
                        len(ratings) == 1 or ratings[0][0] - ratings[1][0] > .1):
                    encodings = (ratings[0][1], "utf-8-sig", "gb18030")
        for encoding in encodings:
            try:
                return contents.decode(encoding)[:MAX_DOCUMENT_TEXT]
            except UnicodeDecodeError as error:
                if error.reason == "unexpected end of data" and error.start >= len(contents) - 4:
                    return contents[:error.start].decode(encoding)[:MAX_DOCUMENT_TEXT]
                continue
    if extension in {".htm", ".html"}:
        with path.open("rb") as handle:
            contents = handle.read(min(size, MAX_DOCUMENT_BYTES))
        return clean_html(contents.decode("utf-8-sig", errors="replace"))[:MAX_DOCUMENT_TEXT]
    if extension == ".pdf":
        from pypdf import PdfReader
        with path.open("rb") as stream:
            reader = PdfReader(stream, strict=False)
            count = len(reader.pages)
            if count == 0:
                return ""
            sample_count = min(count, OCR_PAGES)
            indexes = (list(range(count)) if count <= sample_count else
                       sorted({round(index * (count - 1) / max(1, sample_count - 1))
                               for index in range(sample_count)}))
            text = []
            total = 0
            for index in indexes:
                fragment = (reader.pages[index].extract_text() or "").strip()
                fragment = fragment[:max(0, MAX_DOCUMENT_TEXT - total)]
                if fragment:
                    text.append("[第 %d 页] %s" % (index + 1, fragment))
                    total += len(fragment)
                if total >= MAX_DOCUMENT_TEXT:
                    break
        if total < max(30, len(indexes) * 12):
            try:
                return pdf_ocr_text(path, pages=indexes)
            except (ImportError, ModuleNotFoundError) as error:
                raise RuntimeError("扫描 PDF 需要可选离线 OCR 组件；可在部署时尝试安装：" + str(error)[:120]) from error
        return "\n".join(text)[:MAX_DOCUMENT_TEXT]
    if extension == ".docx":
        import xml.etree.ElementTree as ET
        with zipfile.ZipFile(path) as archive:
            if sum(item.file_size for item in archive.infolist() if item.filename.endswith(".xml")) > MAX_DOCUMENT_BYTES:
                raise ValueError("DOCX 解压后 XML 体积超出安全限制")
            if archive.getinfo("word/document.xml").file_size > MAX_DOCUMENT_XML_BYTES:
                raise ValueError("DOCX 正文过大，无法安全解析")
            xml = archive.read("word/document.xml")
        root = ET.fromstring(xml)
        parts = [item.text or "" for item in root.iter() if item.tag.endswith("}t")]
        return " ".join(parts)[:MAX_DOCUMENT_TEXT]
    return ""


def document_text_controlled(path, root, log, cancel=None):
    path = Path(path)
    if path.suffix.lower() not in {".pdf", ".docx"}:
        return document_text(path)
    temporary = Path(root) / ".studio" / "tmp" / ("document_" + secrets.token_hex(12) + ".txt")
    try:
        estimated = min(600, max(90, int(path.stat().st_size / (128 * 1024)) + 90))
        run_external([str(runtime_python(root)), str(Path(__file__).resolve()), "--read-document",
                      str(root), str(path), str(temporary)], root, log=log, cancel=cancel,
                     timeout=estimated, capture=True, env=shell_env(root, offline=True))
        return temporary.read_text(encoding="utf-8")[:MAX_DOCUMENT_TEXT]
    finally:
        temporary.unlink(missing_ok=True)


def localize_request_assets(root, request, job, cancel=None, log=None, prior=None):
    root = Path(root).resolve()
    job = Path(job).resolve()
    destination = job / "sources"
    destination.mkdir(parents=True, exist_ok=True)
    previous = (prior or {}).get("localized_sources", {})
    mapped = {}
    localized = {}
    for category, files in request.get("files", {}).items():
        output = []
        for name in files:
            if cancel is not None and cancel.is_set():
                raise InterruptedError("复制素材时已停止")
            original = str(name)
            path = Path(original)
            if not path.is_file() and isinstance(previous, dict) and original in previous:
                path = Path(previous[original].get("copy", ""))
            if not path.is_file() or path.is_symlink():
                raise FileNotFoundError("所选素材不可访问或不是普通文件：" + Path(original).name)
            resolved = path.resolve()
            if root == resolved or root in resolved.parents:
                output.append(str(resolved))
                localized[original] = {"copy": str(resolved), "stored_in_workspace": True,
                                       "bytes": resolved.stat().st_size}
                continue
            size = resolved.stat().st_size
            required = MIN_JOB_FREE + size + min(SOURCE_COPY_CHUNK * 4, size)
            if shutil.disk_usage(root).free < required:
                raise RuntimeError("素材 %s 无法安全保存到工作目录，至少还需 %.2f GB 空间" % (
                    resolved.name, required / GB))
            identity = hashlib.sha256((str(resolved).lower() + ":" + str(size) + ":" +
                                       str(resolved.stat().st_mtime_ns)).encode("utf-8")).hexdigest()[:24]
            target = destination / (identity + resolved.suffix.lower())
            signature = file_integrity_hash(resolved)
            if not target.is_file() or target.stat().st_size != size or file_integrity_hash(target) != signature:
                staging = target.with_suffix(target.suffix + ".partial")
                try:
                    with resolved.open("rb") as reader, staging.open("wb") as writer:
                        while True:
                            if cancel is not None and cancel.is_set():
                                raise InterruptedError("素材复制已停止")
                            chunk = reader.read(SOURCE_COPY_CHUNK)
                            if not chunk:
                                break
                            writer.write(chunk)
                    if staging.stat().st_size != size or file_integrity_hash(staging) != signature:
                        raise RuntimeError("素材在复制期间发生了变化：" + resolved.name)
                    os.replace(staging, target)
                finally:
                    staging.unlink(missing_ok=True)
            output.append(str(target))
            mapped[original] = str(target)
            localized[original] = {"copy": str(target), "bytes": size, "sample_hash": signature,
                                   "stored_in_workspace": False}
            if log:
                log("已将素材保存到工作目录：" + resolved.name)
        request["files"][category] = output
    return localized


def clean_html(data):
    data = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)\b[^>]*>.*?</\1>", " ", data)
    data = re.sub(r"(?is)<[^>]+>", " ", data)
    data = html.unescape(data)
    return re.sub(r"\s+", " ", data).strip()


def png_or_video_image(path, output, root, log, cancel=None):
    path = Path(path)
    if path.suffix.lower() in IMAGE_TYPES:
        return path
    flags = [ffmpeg_executable(), "-hide_banner", "-loglevel", "error", "-y", "-i", path,
             "-vf", "select=eq(n\\,0),scale=720:720:force_original_aspect_ratio=decrease",
             "-frames:v", "1", output]
    run_external(flags, root, log=log, cancel=cancel, timeout=FFMPEG_INPUT_TIMEOUT, capture=True)
    return Path(output)


def audio_seconds(path):
    try:
        with wave.open(str(path), "rb") as audio:
            return audio.getnframes() / audio.getframerate()
    except (OSError, wave.Error, ZeroDivisionError):
        return 0.0


def normalized_wave(source, target, root, log, duration=30, cancel=None, timeout=FFMPEG_INPUT_TIMEOUT):
    args = [ffmpeg_executable(), "-hide_banner", "-loglevel", "error", "-nostdin", "-y", "-i", str(source)]
    if duration is not None:
        args.extend(["-t", str(duration)])
    args.extend(["-vn", "-ac", "1", "-ar", str(SPEECH_RATE), "-c:a", "pcm_s16le", str(target)])
    run_external(args, root, log=log, cancel=cancel, timeout=timeout, capture=True)
    return Path(target)


def join_voice_audio(wavs, durations, output):
    if len(wavs) != len(durations):
        raise ValueError("旁白片段与镜头时长的数量不一致")
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(output), "wb") as dest:
        dest.setnchannels(1)
        dest.setsampwidth(2)
        dest.setframerate(SPEECH_RATE)
        for item, seconds in zip(wavs, durations):
            expected = round(seconds * SPEECH_RATE)
            actual = b""
            if item and Path(item).exists():
                with wave.open(str(item), "rb") as handle:
                    if (handle.getnchannels() != 1 or handle.getsampwidth() != 2
                            or handle.getframerate() != SPEECH_RATE):
                        raise ValueError("旁白音频不是 16kHz、16 位、单声道 PCM")
                    if handle.getnframes() > expected:
                        raise ValueError("旁白超过镜头时长，禁止静默截断：" + str(item))
                    actual = handle.readframes(expected)
            if len(actual) > expected * 2:
                actual = actual[:expected * 2]
            dest.writeframesraw(actual)
            rest = expected * 2 - len(actual)
            if rest > 0:
                dest.writeframesraw(bytes(rest))
        dest.writeframes(b"")
    return output


def planned_durations(seconds, count, fps=DEFAULT_FPS):
    if seconds <= 0 or count <= 0 or fps <= 0:
        raise ValueError("总时长、镜头数量和帧率必须大于零")
    frames, remainder = divmod(round(float(seconds) * fps), count)
    if frames < 2 * fps:
        raise ValueError("镜头时长过短，无法完成正常创作")
    return [(frames + (i < remainder)) / fps for i in range(count)]


def narration_units(text):
    return len(re.findall(r"[\u3400-\u9fffA-Za-z0-9]", str(text)))


def reference_terms(text):
    text = str(text).lower()
    chinese = re.findall(r"[\u3400-\u9fff]+", text)
    english = set(re.findall(r"[a-z0-9]{3,}", text))
    terms = set(english)
    for part in chinese:
        terms.update(part[i:i + 2] for i in range(max(0, len(part) - 1)))
        terms.update(part[i:i + 3] for i in range(max(0, len(part) - 2)))
    return terms


def select_reference_snippets(prompt, records, budget=MAX_REFERENCE_BUDGET):
    records = [(str(title).strip()[:110], str(content).strip()) for title, content in records if str(content).strip()]
    if not records or budget < 180:
        return ""
    prompt_words = reference_terms(prompt)
    selections = []
    for origin, (title, content) in enumerate(records):
        paragraphs = [re.sub(r"\s+", " ", fragment).strip() for fragment in
                      re.split(r"(?<=[。！？.!?])\s*|[\n\r]+", content)]
        if not paragraphs:
            paragraphs = [content]
        window = []
        for paragraph in paragraphs:
            for offset in range(0, len(paragraph), 360):
                fragment = paragraph[offset:offset + 360]
                if not fragment.strip():
                    continue
                overlap = len(prompt_words & reference_terms(fragment))
                numbers = bool(re.search(r"\d{4}|\d+(?:[.%％]|万元|公里)", fragment))
                score = overlap * 5 + int(numbers) * 2 + min(2, len(fragment) / 140)
                window.append((score, offset, fragment))
        for rank, (score, offset, fragment) in enumerate(sorted(window, reverse=True)[:5]):
            selections.append((score, origin, rank, title, fragment))
    chosen = []
    used = 0
    for origin, (title, _) in enumerate(records):
        own = [item for item in selections if item[1] == origin]
        if not own:
            continue
        best = max(own, key=lambda item: item[0])
        entry = "%s：%s" % (best[3], best[4])
        allowance = max(90, min(360, budget // max(1, len(records)) - 16))
        entry = entry[:allowance]
        if used + len(entry) + 1 > budget:
            continue
        chosen.append(entry)
        used += len(entry) + 1
        selections.remove(best)
    for item in sorted(selections, key=lambda entry: entry[0], reverse=True):
        if used + 75 > budget:
            break
        entry = "%s（补充）：%s" % (item[3], item[4])
        entry = entry[:min(len(entry), budget - used - 1)]
        if len(entry) > 35:
            chosen.append(entry)
            used += len(entry) + 1
    return "\n".join(chosen)[:budget]


def semantic_timeline(seconds, scenes, fps=DEFAULT_FPS):
    if not scenes:
        return []
    total_frames = round(float(seconds) * fps)
    floor_frames = 2 * fps
    if total_frames < floor_frames * len(scenes):
        return planned_durations(seconds, len(scenes), fps)
    weights = [max(1, narration_units(scene.get("narration", "")) +
                   min(16, len(str(scene.get("visual_prompt", ""))) // 28) +
                   (3 if index in (0, len(scenes) - 1) else 0))
               for index, scene in enumerate(scenes)]
    remaining = total_frames - floor_frames * len(scenes)
    exact = [remaining * weight / sum(weights) for weight in weights]
    extras = [int(value) for value in exact]
    for index in sorted(range(len(extras)), key=lambda i: exact[i] - extras[i], reverse=True)[:remaining - sum(extras)]:
        extras[index] += 1
    return [(floor_frames + value) / fps for value in extras]



def short_narration(text, limit):
    text = re.sub(r"\s+", "", str(text)).strip("，。！？；、 ")
    units = 0
    result = []
    for char in text:
        if re.match(r"[\u3400-\u9fffA-Za-z0-9]", char):
            if units >= limit:
                break
            units += 1
        result.append(char)
    value = "".join(result).rstrip("，。！？；、 ")
    return value + ("。" if value and value[-1] not in "。！？" else "")


def asset_cache_identity(asset):
    if not asset or not isinstance(asset, (tuple, list)) or len(asset) != 2:
        return asset
    kind, filename = asset
    path = Path(filename)
    try:
        stat = path.stat()
        return (kind, str(path.resolve()), stat.st_size, stat.st_mtime_ns, file_integrity_hash(path))
    except OSError:
        return (kind, str(path), "missing")


def scene_cache_key(scene, seconds, aspect, quality, asset, size, fps, signature=""):
    content = (scene.get("narration"), scene.get("visual_prompt"), round(seconds, 5),
               aspect, quality, asset_cache_identity(asset), tuple(size), fps, PIPELINE_VERSION, signature)
    return hashlib.sha256(repr(content).encode("utf-8")).hexdigest()


def wav_rms(path):
    with wave.open(str(path), "rb") as handle:
        if handle.getsampwidth() != 2 or handle.getnchannels() != 1:
            raise ValueError("仅支持 16 位单声道 WAV 检查")
        samples = array.array("h")
        total_energy = 0
        count = 0
        while True:
            raw = handle.readframes(65536)
            if not raw:
                break
            samples.frombytes(raw)
            if sys.byteorder != "little":
                samples.byteswap()
            total_energy += sum(value * value for value in samples)
            count += len(samples)
            samples = array.array("h")
        return math.sqrt(total_energy / count) / 32768.0 if count else 0.0


def generate_music(output, seconds, mood, seed):
    import numpy as np
    chords = {
        "warm": [(0, 4, 7), (5, 9, 12), (9, 12, 16), (7, 11, 14)],
        "calm": [(0, 3, 7), (8, 12, 15), (5, 8, 12), (7, 10, 14)],
        "mysterious": [(0, 3, 6), (10, 13, 17), (7, 10, 14), (8, 11, 15)],
        "energetic": [(0, 4, 7), (7, 11, 14), (9, 12, 16), (5, 9, 12)],
        "inspiring": [(0, 4, 7), (9, 12, 16), (5, 9, 12), (7, 11, 14)],
    }
    value = str(mood).lower().strip()
    palette = next((chords[key] for key in chords if key in value), chords["inspiring"])
    length = int(seconds * SPEECH_RATE)
    base_note = 48 + (seed % 4)
    beat = 0.55 if value != "energetic" else 0.38
    rnd = random.Random(seed)
    phases = [rnd.uniform(0, math.tau) for _ in range(4)]
    chord_table = np.asarray(palette, dtype=np.int32)
    with wave.open(str(output), "wb") as writer:
        writer.setnchannels(1)
        writer.setsampwidth(2)
        writer.setframerate(SPEECH_RATE)
        chunk_size = SPEECH_RATE * 2
        for start in range(0, length, chunk_size):
            t = np.arange(start, min(length, start + chunk_size), dtype=np.float64) / SPEECH_RATE
            bars = np.floor(t / (beat * 4)).astype(np.int32)
            chords_now = chord_table[bars % len(palette)]
            sound = np.zeros(len(t), dtype=np.float64)
            for layer in range(chords_now.shape[1]):
                freq = 440 * 2.0 ** ((base_note + chords_now[:, layer] - 69) / 12)
                phase = math.tau * freq * t + phases[layer]
                sound += .22 * np.sin(phase) + .08 * np.sin(phase * 2 - phases[layer])
            bass = 440 * 2.0 ** ((base_note + chords_now[:, 0] - 81) / 12)
            sound += .20 * np.sin(math.tau * bass * t)
            arp_indexes = np.floor(t / (beat / 2)).astype(np.int32) % chords_now.shape[1]
            arp = chords_now[np.arange(len(t)), arp_indexes]
            arp_freq = 440 * 2.0 ** ((base_note + arp + 12 - 69) / 12)
            sound += .14 * np.sin(math.tau * arp_freq * t) * np.exp(-4 * ((t % (beat / 2)) / beat))
            envelope = np.minimum(1, np.minimum(t / 1.2, np.maximum(0, (seconds - t) / 1.6)))
            swell = .65 + .15 * np.sin(math.tau * ((t % (beat * 4)) / (beat * 4)))
            samples = (np.clip(sound * swell * envelope, -1, 1) * 13000).astype("<i2")
            writer.writeframesraw(samples.tobytes())
        writer.writeframes(b"")
    return output

def assess_visual_similarity(scores):
    if len(scores) < 5 or any(not math.isfinite(float(value)) for value in scores):
        raise RuntimeError("语义审校分数不完整，无法完成有效比较")
    match, subject = float(scores[0]), float(scores[1])
    negatives = [float(value) for value in scores[2:]]
    negative_peak = max(negatives)
    margin = max(match, subject) - negative_peak
    required_cosine = max(MIN_CLIP_ABSOLUTE_COSINE,
                          min(MIN_CLIP_COSINE + .045, max(MIN_CLIP_COSINE - .018,
                                                         negative_peak + MIN_CLIP_MARGIN)))
    required_margin = max(MIN_CLIP_ABSOLUTE_MARGIN,
                          min(MIN_CLIP_MARGIN + .018, MIN_CLIP_MARGIN + max(0.0, negative_peak - .14) * .08))
    subject_margin = subject - negative_peak
    passed = (match >= required_cosine and margin >= required_margin and
              subject_margin >= MIN_CLIP_ABSOLUTE_MARGIN)
    return {"cosine": round(match, 4), "subject_cosine": round(subject, 4),
            "negative_peak": round(negative_peak, 4), "margin": round(margin, 4),
            "subject_margin": round(subject_margin, 4),
            "required_cosine": round(required_cosine, 4),
            "required_margin": round(required_margin, 4),
            "status": REVIEW_PASS if passed else REVIEW_FAIL,
            "method": "CLIP 对比原始镜头、主体和负面锚点的自适应启发式评分，无法核实数量、身份或真实动作",
            "passed": bool(passed)}


class LocalModels:
    def __init__(self, root, notify, stop, quality="智能", resources=None):
        self.root = Path(root)
        self.notify = notify
        self.stop = stop
        self.quality = quality
        self.resources = resources if resources is not None else ResourceGovernor(root)
        self.torch = importlib.import_module("torch")
        self.torch.set_num_threads(available_threads())
        try:
            self.torch.set_num_interop_threads(max(1, min(2, available_threads())))
        except RuntimeError:
            pass
        self.gpu = gpu_info()
        self.selected_gpu = None
        self.device = "cpu"
        selected = select_torch_gpu(self.torch, CUDA_MIN_FREE_BYTES + MIN_GPU_HEADROOM)
        if selected:
            try:
                self.torch.cuda.set_device(selected["index"])
                self.selected_gpu = selected["index"]
                self.gpu = {**self.gpu, **selected}
                self.device = "cuda"
                self.resources.attach_cuda(self.torch, self.selected_gpu)
            except (RuntimeError, AssertionError, ValueError):
                self.device = "cpu"
                self.selected_gpu = None
                self.resources.attach_cuda()
        self.dtype = self.torch.float16 if self.device == "cuda" else self.torch.float32
        self.model_choices = {item[2]: item[2] for item in MODEL_SPECS}
        free_ram = memory_info()["available"]
        selected_free = 0
        if self.device == "cuda":
            try:
                selected_free = self.torch.cuda.mem_get_info()[0]
            except (RuntimeError, AssertionError):
                pass
        if quality == "精细":
            for role, optional_folder in OPTIONAL_MODEL_FOLDERS.items():
                minimum_ram = 16 * GB if role in {"director", "listener"} else 12 * GB
                minimum_gpu = 9 * GB if role == "painter" else 6 * GB
                if (free_ram >= minimum_ram and (self.device != "cuda" or selected_free >= minimum_gpu)
                        and optional_model_verified(model_path(self.root, optional_folder), role)):
                    self.model_choices[role] = optional_folder
                    self.notify("精细模式启用经过摘要校验的选装模型：" + role)
        self.tokenizer = None
        self.director = None
        self.painter = None
        self.inspector = None
        self.inspector_processor = None
        self.inspector_failed = False
        self.listener = None
        self.listener_processor = None
        label = ("GPU %d · %s" % (self.selected_gpu, self.gpu["name"]) if self.device == "cuda"
                 else "CPU 资源保护模式")
        self.notify("运行设备：" + label)

    def model_folder(self, role):
        return model_path(self.root, self.model_choices.get(role, role))

    def revert_model(self, role, error):
        if self.model_choices.get(role, role) == role:
            return False
        self.notify("选装模型不兼容当前设备，改用已验收的内置模型：" + role + " / " + str(error)[:140])
        self.model_choices[role] = role
        self.unload_director() if role == "director" else None
        self.unload_painter() if role == "painter" else None
        self.unload_inspector() if role == "inspector" else None
        if role == "listener":
            self.listener = self.listener_processor = None
        return True

    def check_stop(self):
        if self.stop.is_set():
            raise InterruptedError("已停止")

    def unload_director(self):
        self.director = None
        self.tokenizer = None
        gc.collect()
        try:
            if self.torch.cuda.is_available():
                self.torch.cuda.empty_cache()
        except (RuntimeError, AssertionError):
            pass

    def unload_painter(self):
        self.painter = None
        gc.collect()
        try:
            if self.torch.cuda.is_available():
                self.torch.cuda.empty_cache()
        except (RuntimeError, AssertionError):
            pass

    def unload_inspector(self):
        self.inspector = None
        self.inspector_processor = None
        gc.collect()

    def switch_to_cpu(self, reason):
        self.notify("GPU 资源不足，自动切换 CPU：" + str(reason)[:140])
        self.unload_director()
        self.unload_painter()
        if self.inspector is not None and memory_info()["available"] < MODEL_SWITCH_FREE_BYTES:
            self.unload_inspector()
        self.device = "cpu"
        self.selected_gpu = None
        self.resources.attach_cuda()
        self.dtype = self.torch.float32

    def load_director(self):
        if self.director is not None:
            return
        self.resources.adaptive_pause("director_load", self.stop, self.notify)
        self.resources.ensure("director_load", required=MIN_DIRECTOR_USABLE_RAM)
        if self.painter is not None:
            self.unload_painter()
        if self.inspector is not None and memory_info()["available"] < MODEL_SWITCH_FREE_BYTES:
            self.unload_inspector()
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.notify("加载本地中文导演模型")
        folder = str(self.model_folder("director"))
        for attempt in range(2):
            self.check_stop()
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(folder, local_files_only=True, use_fast=True)
                self.director = AutoModelForCausalLM.from_pretrained(
                    folder, torch_dtype=self.dtype, local_files_only=True, low_cpu_mem_usage=True)
                self.director.to(self.device)
                self.director.eval()
                return
            except (RuntimeError, MemoryError) as error:
                self.unload_director()
                if self.device == "cuda" and is_memory_error(error) and attempt == 0:
                    self.switch_to_cpu(error)
                    continue
                if self.revert_model("director", error) and attempt == 0:
                    folder = str(self.model_folder("director"))
                    continue
                if is_memory_error(error):
                    raise RuntimeError("本机剩余内存不足，无法加载中文文案模型") from error
                raise

    def chat(self, messages, tokens=650):
        self.check_stop()
        for attempt in range(2):
            self.load_director()
            payload = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            batch = None
            try:
                budget = min(MAX_DIRECTOR_CONTEXT, max(2048, int(self.tokenizer.model_max_length)
                              if 0 < self.tokenizer.model_max_length < 100000 else MAX_DIRECTOR_CONTEXT))
                batch = self.tokenizer([payload], return_tensors="pt", truncation=True,
                                       max_length=budget).to(self.device)
                with self.torch.inference_mode():
                    sample = self.director.generate(**batch, max_new_tokens=tokens, do_sample=True,
                                                    temperature=0.60, top_p=0.90, repetition_penalty=1.12,
                                                    pad_token_id=self.tokenizer.eos_token_id)
                return self.tokenizer.decode(sample[0][batch.input_ids.shape[1]:], skip_special_tokens=True).strip()
            except (RuntimeError, MemoryError) as error:
                batch = None
                if self.device == "cuda" and is_memory_error(error) and attempt == 0:
                    self.switch_to_cpu(error)
                    continue
                if is_memory_error(error):
                    raise RuntimeError("本机剩余内存不足，无法完成文案推理") from error
                raise

    def plan(self, prompt, reference, scenes, seconds):
        task = ("你是专业短视频导演。请制作" + str(scenes) + "镜头。"
                "只输出合法JSON，对象字段为"
                '{"title":"中文标题","mood":"warm/calm/mysterious/energetic/inspiring",'
                '"scenes":[{"narration":"自然中文旁白","visual_prompt":"详细英文画面描述","seconds":6}]}。'
                "镜头应相互衔接，旁白每幕不重复、不编造事实。画面描述应包括可见主体、动作、景别、光线和构图。"
                "优先准确遵守用户的主体、人物、地点、首尾画面与限制。"
                f"共{scenes}幕、约{seconds}秒。用户需求：{prompt[:1400]}。"
                f"精选参考片段：{reference[:MAX_REFERENCE_BUDGET]}")
        accepted = None
        best = None
        for attempt in range(2):
            self.check_stop()
            answer = self.chat([{"role": "system", "content": "你是严谨的电影分镜规划和JSON生成器。"},
                                {"role": "user", "content": task + ("请修正JSON语法和缺漏字段。" if attempt else "")}],
                               tokens=min(1500, 260 + 230 * scenes))
            result = extract_json_object(answer)
            if isinstance(result, dict) and isinstance(result.get("scenes"), list):
                if best is None or len(result["scenes"]) > len(best.get("scenes", [])):
                    best = result
            if validate_plan(result, scenes):
                accepted = result
                break
            self.notify("检测到分镜字段缺失，自动修补")
        if not accepted:
            accepted = normalize_plan(best, prompt, scenes, seconds)
            self.notify("已保留模型有效分镜并修复缺漏")
        planned = normalize_plan(accepted, prompt, scenes, seconds)
        for entry in planned["scenes"]:
            visual = str(entry.get("visual_prompt", ""))
            if len(re.findall(r"[\u3400-\u9fff]", visual)) < 5:
                continue
            try:
                response = self.chat([
                    {"role": "system", "content": "Translate a visual scene description into concise English for image diffusion. Preserve all people, objects, colors, counts, actions, places and prohibitions. Output only the English description."},
                    {"role": "user", "content": visual[:360] + "\n原始要求不可更改：" + prompt[:320]}
                ], tokens=180)
                constraints = visual_constraints(visual + " " + prompt)
                if len(response) > 25 and len(re.findall(r"[\u3400-\u9fff]", response)) < len(response) // 8:
                    if visual_constraints_retained(response, constraints):
                        entry["visual_prompt"] = response[:420]
                        entry["translation_status"] = "explicit_attributes_verified"
                    else:
                        entry["translation_status"] = "original_kept_to_preserve_constraints"
            except InterruptedError:
                raise
            except (RuntimeError, OSError, ValueError) as error:
                self.notify("保留原画面描述，翻译模型未能确认所有约束：" + str(error)[:80])
        return planned

    def refine_visual(self, original, review, attempt, user_request):
        base = refine_visual_prompt(original, review, attempt, user_request)
        if attempt == 0:
            return base
        try:
            failure = review_failure_type(review)
            proposal = self.chat([
                {"role": "system", "content": "You repair an image-generation description. Output only English, without adding or removing any people, colors, objects, counts, actions or other constraints. Do not change the user's intent."},
                {"role": "user", "content": "Original scene: " + original[:420] + "\nReason: " + failure +
                 "\nUser restrictions: " + user_request[:380] +
                 "\nRewrite to make the requested subjects clearer; output a single visual description."}
            ], tokens=230)
            required = visual_constraints(original + " " + user_request)
            if 30 <= len(proposal) <= 540 and visual_constraints_retained(proposal, required):
                return (proposal.strip() + " Original constraints: " + original[:260] +
                        " Fixed user attributes: " + ", ".join(required[:10]))[:700]
        except InterruptedError:
            raise
        except (RuntimeError, ValueError, OSError) as error:
            self.notify("修复建议已改用约束保留规则：" + str(error)[:100])
        return base

    def load_painter(self):
        if self.painter is not None:
            return
        self.resources.adaptive_pause("painter_load", self.stop, self.notify)
        self.resources.ensure("painter_load", required=MIN_PAINTER_USABLE_RAM)
        if self.director is not None:
            self.unload_director()
        if self.inspector is not None and memory_info()["available"] < MODEL_SWITCH_FREE_BYTES:
            self.unload_inspector()
        from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
        self.notify("加载本地图像扩散模型")
        for attempt in range(2):
            self.check_stop()
            try:
                self.painter = DiffusionPipeline.from_pretrained(str(self.model_folder("painter")),
                                                                 torch_dtype=self.dtype, local_files_only=True,
                                                                 low_cpu_mem_usage=True)
                if hasattr(self.painter, "scheduler"):
                    self.painter.scheduler = DPMSolverMultistepScheduler.from_config(self.painter.scheduler.config)
                if self.device == "cpu" and hasattr(self.painter, "enable_attention_slicing"):
                    self.painter.enable_attention_slicing()
                self.painter.to(self.device)
                self.painter.set_progress_bar_config(disable=True)
                return
            except (RuntimeError, MemoryError) as error:
                self.unload_painter()
                if self.device == "cuda" and is_memory_error(error) and attempt == 0:
                    self.switch_to_cpu(error)
                    continue
                if self.revert_model("painter", error) and attempt == 0:
                    continue
                if is_memory_error(error):
                    raise RuntimeError("本机剩余内存不足，无法加载图像生成模型") from error
                raise

    def paint(self, prompt, output, seed, mode, aspect="横屏 16:9"):
        self.check_stop()
        self.resources.adaptive_pause("image_generation", self.stop, self.notify)
        self.resources.budget("image_generation", ram_bytes=MIN_PAINTER_USABLE_RAM,
                              disk_bytes=64 * 1024 * 1024)
        self.load_painter()
        try:
            gpu_free = self.torch.cuda.mem_get_info()[0] if self.device == "cuda" else 0
        except (RuntimeError, AssertionError):
            gpu_free = 0
        resolution, steps = self.resources.image_profile(mode, self.device, gpu_free)
        ratio = 9 / 16 if "竖屏" in aspect else 1 if "方形" in aspect else 16 / 9
        pixels = min(MAX_IMAGE_PIXELS, resolution ** 2)
        width = max(MIN_IMAGE_DIMENSION, int(math.sqrt(pixels * ratio)) // 8 * 8)
        height = max(MIN_IMAGE_DIMENSION, int(math.sqrt(pixels / ratio)) // 8 * 8)
        pixels = width * height
        self.notify("自适应生图：%d×%d · %d 步 · %s" % (width, height, steps, self.device))
        generator = self.torch.Generator(device=self.device).manual_seed(int(seed))
        params = {"prompt": prompt, "width": width, "height": height,
                  "num_inference_steps": steps, "guidance_scale": 7.0, "generator": generator}
        try:
            with self.torch.inference_mode():
                result = self.painter(**params).images[0]
        except (RuntimeError, MemoryError) as error:
            if not is_memory_error(error):
                raise
            if self.device != "cuda":
                raise RuntimeError("CPU 内存不足，已停止图像生成以免系统受影响") from error
            self.torch.cuda.empty_cache()
            resized_pixels = max(MIN_IMAGE_DIMENSION ** 2, int(pixels * .60))
            params.update({"width": max(MIN_IMAGE_DIMENSION, int(math.sqrt(resized_pixels * ratio)) // 8 * 8),
                           "height": max(MIN_IMAGE_DIMENSION, int(math.sqrt(resized_pixels / ratio)) // 8 * 8),
                           "num_inference_steps": min(steps, 12),
                           "generator": self.torch.Generator(device="cuda").manual_seed(int(seed))})
            try:
                self.notify("GPU 显存不足，自动降分辨率重试")
                with self.torch.inference_mode():
                    result = self.painter(**params).images[0]
            except (RuntimeError, MemoryError) as gpu_retry_error:
                if not is_memory_error(gpu_retry_error):
                    raise
                self.switch_to_cpu(gpu_retry_error)
                self.load_painter()
                fallback_pixels = MIN_IMAGE_DIMENSION * MIN_IMAGE_DIMENSION * 2
                params.update({"width": max(MIN_IMAGE_DIMENSION, int(math.sqrt(fallback_pixels * ratio)) // 8 * 8),
                               "height": max(MIN_IMAGE_DIMENSION, int(math.sqrt(fallback_pixels / ratio)) // 8 * 8),
                               "num_inference_steps": min(8, steps),
                               "generator": self.torch.Generator(device="cpu").manual_seed(int(seed))})
                try:
                    with self.torch.inference_mode():
                        result = self.painter(**params).images[0]
                except (RuntimeError, MemoryError) as retry_error:
                    if is_memory_error(retry_error):
                        raise RuntimeError("CPU 也无法安全生成图像，已暂停避免影响其他程序") from retry_error
                    raise
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        result.save(output)
        return output

    def load_inspector(self):
        if self.inspector is not None:
            return
        self.resources.adaptive_pause("inspector_load", self.stop, self.notify)
        self.resources.ensure("inspector_load", required=MIN_INSPECTOR_USABLE_RAM)
        if self.inspector_failed:
            raise RuntimeError("画面语义审校尚未通过：设备资源不足或 CLIP 模型加载失败")
        from transformers import CLIPModel, CLIPProcessor
        folder = str(self.model_folder("inspector"))
        self.notify("加载本地画面审校模型")
        failure = None
        for attempt in range(2):
            try:
                free = memory_info()["available"]
                if free and free < MODEL_SWITCH_FREE_BYTES and self.painter is not None:
                    self.notify("为语义审校释放图像生成模型占用的内存")
                    self.unload_painter()
                self.inspector_processor = CLIPProcessor.from_pretrained(
                    folder, local_files_only=True, use_fast=False)
                self.inspector = CLIPModel.from_pretrained(
                    folder, local_files_only=True, torch_dtype=self.torch.float32)
                self.inspector.to("cpu")
                self.inspector.eval()
                return
            except (RuntimeError, MemoryError, OSError) as error:
                failure = error
                self.inspector = None
                self.inspector_processor = None
                if attempt == 0:
                    self.revert_model("inspector", error)
                    folder = str(self.model_folder("inspector"))
                self.unload_painter()
        self.inspector_failed = True
        raise RuntimeError("画面语义审校无法完成，不会把普通图像检查冒充 AI 审校：%s" % failure) from failure

    def image_similarity(self, picture, description):
        self.check_stop()
        from PIL import Image
        self.load_inspector()
        focus = re.split(r"[.;]", description.strip(), maxsplit=1)[0].strip()[:150]
        prompts = [description[:220], focus or description[:150],
                   "a completely empty flat color", "random noise and corrupted pixels",
                   "unrecognizable blurry unrelated objects"]
        with Image.open(picture) as image:
            batch = self.inspector_processor(text=prompts, images=image.convert("RGB"),
                                             return_tensors="pt", padding=True, truncation=True)
        with self.torch.inference_mode():
            picture_features = self.inspector.get_image_features(pixel_values=batch["pixel_values"])
            text_features = self.inspector.get_text_features(input_ids=batch["input_ids"],
                                                             attention_mask=batch["attention_mask"])
            picture_features = picture_features / picture_features.norm(dim=-1, keepdim=True).clamp_min(1e-8)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True).clamp_min(1e-8)
            scores = (picture_features @ text_features.T)[0].tolist()
        return assess_visual_similarity(scores)

    def match_asset_scores(self, scene_prompts, image_paths):
        self.check_stop()
        if not scene_prompts or not image_paths:
            return []
        from PIL import Image, ImageOps
        self.load_inspector()
        strings = [str(prompt).strip()[:240] or "a cinematic scene" for prompt in scene_prompts]
        encoded = self.inspector_processor(text=strings, return_tensors="pt", padding=True, truncation=True)
        with self.torch.inference_mode():
            text_features = self.inspector.get_text_features(input_ids=encoded["input_ids"],
                                                            attention_mask=encoded["attention_mask"])
            text_features = text_features / text_features.norm(dim=-1, keepdim=True).clamp_min(1e-8)
        result = []
        for filename in image_paths:
            self.check_stop()
            try:
                with Image.open(filename) as source:
                    source.draft("RGB", (UI_PREVIEW_IMAGE_LIMIT, UI_PREVIEW_IMAGE_LIMIT))
                    photo = ImageOps.exif_transpose(source).convert("RGB")
                    photo.thumbnail((UI_PREVIEW_IMAGE_LIMIT, UI_PREVIEW_IMAGE_LIMIT))
                    pixels = self.inspector_processor(images=photo, return_tensors="pt")
                with self.torch.inference_mode():
                    image_features = self.inspector.get_image_features(pixel_values=pixels["pixel_values"])
                    image_features = image_features / image_features.norm(dim=-1, keepdim=True).clamp_min(1e-8)
                    scores = (image_features @ text_features.T)[0].tolist()
                result.append([float(value) for value in scores])
            except InterruptedError:
                raise
            except (OSError, ValueError, RuntimeError) as error:
                self.notify("素材语义匹配跳过一个无法读取的预览：" + str(error)[:100])
                result.append(None)
        return result

    def transcribe(self, source, work, logger, max_seconds=None, include_timestamps=True, language=None):
        self.check_stop()
        import numpy as np
        source = Path(source)
        stat = source.stat()
        maximum = max(1.0, float(max_seconds) if max_seconds is not None
                      else ASR_WINDOW_SECONDS * MAX_ASR_USER_WINDOWS)
        windows_count = min(MAX_ASR_USER_WINDOWS, math.ceil(maximum / ASR_WINDOW_SECONDS))
        fingerprint = hashlib.sha256(json.dumps([
            str(source.resolve()), stat.st_size, stat.st_mtime_ns,
            file_integrity_hash(source), MODEL_REVISIONS[MODEL_SPECS[2][1]],
            SPEECH_RATE, ASR_WINDOW_SECONDS, windows_count, include_timestamps, language or "auto",
            str(self.model_folder("listener"))],
            ensure_ascii=False).encode("utf-8")).hexdigest()
        cache = self.root / ".studio" / "cache" / "transcripts"
        cache.mkdir(parents=True, exist_ok=True)
        record_path = cache / (fingerprint + ".json")
        previous = read_json(record_path, {})
        if previous.get("fingerprint") == fingerprint and isinstance(previous.get("text"), str):
            self.notify("复用已完成的离线声音识别结果")
            return previous["text"]
        pcm = Path(work) / ("audio_" + fingerprint[:16] + ".wav")
        normalized_wave(source, pcm, self.root, logger, duration=maximum,
                        cancel=self.stop, timeout=max(FFMPEG_INPUT_TIMEOUT, int(maximum * 2)))
        candidates = []
        with wave.open(str(pcm), "rb") as audio:
            for segment in range(windows_count):
                self.check_stop()
                raw = audio.readframes(SPEECH_RATE * ASR_WINDOW_SECONDS)
                if not raw:
                    break
                values = np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0
                if len(values) < SPEECH_RATE // 4:
                    continue
                windows = values[:len(values) // 1600 * 1600].reshape(-1, 1600)
                energy = np.sqrt(np.mean(windows * windows, axis=1))
                if float(np.percentile(energy, 75)) < .004 or float(np.mean(energy > .007)) < .07:
                    continue
                candidates.append((segment, values))
        if not candidates:
            atomic_json(record_path, {"fingerprint": fingerprint, "text": "", "speech_windows": 0,
                                      "checked": now_stamp()})
            return ""
        from transformers import WhisperForConditionalGeneration, WhisperProcessor
        if self.listener is None:
            self.notify("加载本地语音识别模型")
            folder = str(self.model_folder("listener"))
            self.listener_processor = WhisperProcessor.from_pretrained(folder, local_files_only=True)
            self.listener = WhisperForConditionalGeneration.from_pretrained(folder, local_files_only=True)
            self.listener.to("cpu")
            self.listener.eval()
        transcriptions = []
        for segment, values in candidates:
            self.check_stop()
            data = self.listener_processor(values, sampling_rate=SPEECH_RATE, return_tensors="pt")
            with self.torch.inference_mode():
                params = {"max_new_tokens": 120, "task": "transcribe"}
                if language:
                    params["language"] = language
                ids = self.listener.generate(data.input_features, **params)
            content = self.listener_processor.batch_decode(ids, skip_special_tokens=True)[0].strip()
            if content:
                transcriptions.append(("[%d秒] " % (segment * ASR_WINDOW_SECONDS) if include_timestamps else "")
                                      + content)
        result = " ".join(transcriptions)
        atomic_json(record_path, {"fingerprint": fingerprint, "text": result,
                                  "speech_windows": len(candidates), "checked": now_stamp()})
        files = sorted(cache.glob("*.json"), key=lambda item: item.stat().st_mtime, reverse=True)
        for old in files[MAX_ASR_CACHE_ENTRIES:]:
            old.unlink(missing_ok=True)
        return result

    def close(self):
        self.unload_painter()
        self.unload_inspector()
        self.listener = None
        self.listener_processor = None
        self.unload_director()
        gc.collect()


class StudioJob:
    def __init__(self, root, request, notify, cancel, log, emit=None):
        self.root = Path(root)
        self.request = request
        self.notify = notify
        self.cancel = cancel
        self.log = log
        self.emit = emit or (lambda payload: None)
        self.resources = ResourceGovernor(root)
        self.piper_worker = None
        self.feature_warnings = set()
        self.run_started = time.monotonic()
        digest = request_fingerprint(request)
        jobs_folder = self.root / ".studio" / "jobs"
        old = None
        for candidate in sorted(jobs_folder.glob("*/job.json"), reverse=True)[:20]:
            details = read_json(candidate, {})
            if (details.get("request_digest") == digest and details.get("app") in {APP_VERSION, "1.5.0"}
                    and details.get("status") in ("失败", "已停止", "运行中")):
                old = (candidate.parent, details)
                break
        self.timestamp = now_stamp()
        self.name = slug(request["prompt"], 22)
        self.job = old[0] if old else jobs_folder / (self.timestamp + "_" + self.name)
        self.job.mkdir(parents=True, exist_ok=True)
        self.result_dir = Path(old[1]["result_dir"]) if old and old[1].get("result_dir") else self.root / "成品" / self.job.name
        self.result_dir.mkdir(parents=True, exist_ok=True)
        self.data = old[1] if old else {"app": APP_VERSION, "started": datetime.datetime.now().isoformat(),
                                         "request": request, "request_digest": digest,
                                         "system": {"memory": memory_info(), "gpu": gpu_info(),
                                                    "cpu_count": os.cpu_count()}, "events": [], "warnings": []}
        self.data.update({"status": "运行中", "result_dir": str(self.result_dir),
                          "resumed": bool(old), "request_digest": digest})
        self.data.setdefault("warnings", [])
        atomic_json(self.job / "job.json", self.data)
        self.models = None
        self.ffmpeg = ffmpeg_executable()
        self.fps = DEFAULT_FPS
        old_size = self.data.get("resolution")
        old_fps = self.data.get("fps")
        if isinstance(old_size, list) and len(old_size) == 2 and all(
                isinstance(value, int) and value >= 256 and value % 2 == 0 for value in old_size):
            self.size = tuple(old_size)
        else:
            self.size = self.choose_size()
        if isinstance(old_fps, int) and 12 <= old_fps <= 60:
            self.fps = old_fps
        self.data["resolution"] = list(self.size)
        self.data["fps"] = self.fps
        atomic_json(self.job / "job.json", self.data)
        diagnostic = read_json(self.root / ".studio" / "ready.json", {}).get("diagnostic") or read_json(
            self.root / ".studio" / "basic_ready.json", {}).get("diagnostic", {})
        self.voice_backend = diagnostic.get("voice_backend", "sapi")
        self.cache_signature = hashlib.sha256((model_signature(self.root) + self.voice_backend +
                                                PIPELINE_VERSION).encode("utf-8")).hexdigest()
        self.capabilities = require_request_capabilities(self.root, request)
        self.data["capabilities_at_start"] = self.capabilities
        self.data["review_summary"] = {"approved": 0, "user_semantic_warning": 0, "not_checked": 0}
        self.scene_extra_assets = {}
        self.motion_safe_scenes = set()
        atomic_json(self.job / "job.json", self.data)

    def warn(self, message):
        if message not in self.data["warnings"]:
            self.data["warnings"].append(message)
        self.log(message)

    def assign_assets(self, scenes):
        count = len(scenes)
        previous = self.data.get("assigned_assets")
        request_signature = hashlib.sha256(json.dumps(self.request.get("files", {}), ensure_ascii=False,
                                                      sort_keys=True).encode("utf-8")).hexdigest()
        if (isinstance(previous, dict) and previous.get("count") == count and
                previous.get("request_signature") == request_signature):
            stored = previous.get("items")
            if isinstance(stored, dict):
                recovered = {}
                for key, value in stored.items():
                    if (str(key).isdigit() and int(key) < count and isinstance(value, list)
                            and len(value) == 2 and value[0] in {"image", "video"}
                            and Path(value[1]).is_file()):
                        recovered[int(key)] = tuple(value)
                    else:
                        break
                else:
                    addition = previous.get("additional", {})
                    if isinstance(addition, dict) and all(
                            str(key).isdigit() and int(key) < count and isinstance(values, list) and
                            all(isinstance(pair, list) and len(pair) == 2 and pair[0] in {"image", "video"}
                                and Path(pair[1]).is_file() for pair in values)
                            for key, values in addition.items()):
                        self.scene_extra_assets = {int(key): [tuple(pair) for pair in values]
                                                   for key, values in addition.items()}
                        self.log("已恢复上次确定的镜头素材分配与附加素材")
                        return recovered
        supplied = self.request["files"]
        assigned = {}
        if supplied.get("首帧"):
            assigned[0] = ("image", supplied["首帧"][0])
        if supplied.get("尾帧"):
            assigned[count - 1] = ("image", supplied["尾帧"][0])
        available = [index for index in range(count) if index not in assigned]
        candidates = ([('video', name) for name in supplied.get('视频', [])]
                      + [('image', name) for name in supplied.get('图片', [])])
        chosen = set()
        if available and len(candidates) > 1:
            try:
                self.log("根据分镜语义自动匹配用户素材")
                pool = candidates[:min(len(candidates), ASSET_MATCH_LIMIT,
                                       max(len(available), len(available) * ASSET_MATCH_FACTOR))]
                paths = []
                indexes = []
                for source_index, (kind, filename) in enumerate(pool):
                    if self.cancel.is_set():
                        raise InterruptedError("已停止")
                    if kind == 'video':
                        preview = self.job / ("asset_match_%02d.png" % source_index)
                        try:
                            if not preview.is_file():
                                png_or_video_image(filename, preview, self.root, self.log, self.cancel)
                            filename = str(preview)
                        except (RuntimeError, OSError, TimeoutError) as error:
                            self.log("视频素材无法参与自动匹配：" + str(error)[:160])
                            continue
                    paths.append(filename)
                    indexes.append(source_index)
                scores = (self.models.match_asset_scores(
                    [scenes[index]["visual_prompt"] for index in available], paths)
                    if self.capabilities["semantic_review"] else [])
                pairs = []
                for asset_i, row in enumerate(scores):
                    if row is None:
                        continue
                    for scene_i, similarity in enumerate(row):
                        if math.isfinite(similarity):
                            pairs.append((similarity, indexes[asset_i], available[scene_i]))
                pairs.sort(key=lambda item: item[0], reverse=True)
                for similarity, source_index, scene_index in pairs:
                    if scene_index not in assigned and source_index not in chosen:
                        assigned[scene_index] = candidates[source_index]
                        chosen.add(source_index)
                        self.log("镜头 %d 匹配素材 %s（相关性 %.3f）" % (
                            scene_index + 1, Path(candidates[source_index][1]).name, similarity))
            except InterruptedError:
                raise
            except (OSError, ValueError, RuntimeError, MemoryError) as error:
                self.log("智能素材匹配不可用，按输入顺序继续：" + str(error)[:220])
        remaining = (index for index in available if index not in assigned)
        for source_index, candidate in enumerate(candidates):
            if source_index in chosen:
                continue
            scene_index = next(remaining, None)
            if scene_index is None:
                break
            assigned[scene_index] = candidate
            chosen.add(source_index)
        unused = [asset for source_index, asset in enumerate(candidates) if source_index not in chosen]
        native_available = (self.request.get("visual_mode", "").startswith("原生AI视频")
                            and self.capabilities["native_video"])
        if not self.capabilities["image_generation"] and not native_available:
            alternatives = [("video", name) for name in supplied.get("视频", [])] + [
                ("image", name) for kind in ("图片", "首帧", "尾帧") for name in supplied.get(kind, [])]
            if not alternatives and len(assigned) < count:
                raise RuntimeError("缺少离线画面生成模型和可用素材，请先完成扩展安装")
            for scene_index in range(count):
                if scene_index not in assigned:
                    assigned[scene_index] = alternatives[scene_index % len(alternatives)]
            self.warn("使用用户素材剪辑；扩展 AI 审校未验收时将明确标记为未审校，不冒充语义通过")
        durations = [float(scene.get("seconds", self.request["duration"] / count)) for scene in scenes]
        self.scene_extra_assets = distribute_unused_assets(scenes, assigned, unused, self.request,
                                                          durations, self.fps)
        if unused:
            self.log("已为 %d 个额外素材分配可观看的子镜头，不会静默丢弃" % len(unused))
        self.data["assigned_assets"] = {"count": count, "request_signature": request_signature,
                                        "items": {str(index): list(value) for index, value in assigned.items()},
                                        "additional": {str(i): [list(item) for item in values]
                                                       for i, values in self.scene_extra_assets.items()}}
        atomic_json(self.job / "job.json", self.data)
        return assigned

    def publish_event(self, kind, **fields):
        self.emit({"type": kind, **fields})

    def rewrite_narration(self, text, seconds, strength=1):
        limit = max(6, min(int(max(1, seconds - SPEECH_END_MARGIN) * 3.2 / strength),
                           int(narration_units(text) * .85)))
        if narration_units(text) <= limit:
            return text
        try:
            result = self.models.chat([
                {"role": "system", "content": "你是中文短视频配音编辑，只输出一句精炼的旁白，不增加新事实。"},
                {"role": "user", "content": "将以下旁白压缩为不超过%d个汉字，不要标题、解释或引号：%s" % (limit, text[:220])}
            ], tokens=100)
            revised = result.splitlines()[0].strip().strip('"“”') if result else ""
            if narration_units(revised) >= 3 and narration_units(revised) <= limit:
                return revised
        except InterruptedError:
            raise
        except Exception as error:
            self.log("旁白缩写改用规则兜底：" + str(error)[:180])
        return short_narration(text, limit)

    def fit_speech(self, scene, stem, duration):
        text = scene["narration"]
        for attempt in range(3):
            self.models.check_stop()
            track = self.create_speech(text, stem)
            length = audio_seconds(track)
            maximum = duration - SPEECH_END_MARGIN
            if length <= maximum:
                scene["narration"] = text
                return track
            ratio = length / maximum
            if ratio <= MAX_SPEECH_SPEEDUP:
                compressed = self.job / (stem + "_fitted.wav")
                run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(track),
                              "-filter:a", "atempo=%.5f" % (ratio * 1.01), "-c:a", "pcm_s16le",
                              "-ar", str(SPEECH_RATE), "-ac", "1", str(compressed)],
                             self.root, log=self.log, cancel=self.cancel, timeout=120, capture=True)
                if audio_seconds(compressed) <= duration:
                    scene["narration"] = text
                    return compressed
            if attempt < 2:
                text = self.rewrite_narration(text, maximum, strength=1.3 + attempt * .3)
                scene["narration"] = text
                self.log("旁白超出单镜头时长，已缩写并重新合成：第 %d 次" % (attempt + 1))
                atomic_json(self.job / "storyboard.json", self.active_plan)
        raise RuntimeError("旁白仍超过镜头时长，已停止避免被截断；请检查该段文字与语音模型")

    def validate_clip(self, clip, seconds):
        if not clip.is_file() or clip.stat().st_size < 1500:
            raise RuntimeError("视频片段尚未成功写入")
        output = run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-xerror",
                               "-i", str(clip), "-map", "0:v:0", "-an", "-progress", "pipe:1",
                               "-f", "null", "-"], self.root, cancel=self.cancel,
                              timeout=max(FFMPEG_INPUT_TIMEOUT, int(seconds * 8)), capture=True)
        times = re.findall(r"out_time_(?:us|ms)=(\d+)", output)
        frames = re.findall(r"(?:^|\n)frame=\s*(\d+)", output)
        if not times or not frames:
            raise RuntimeError("视频片段无法完成逐帧解码和长度检查")
        duration = int(times[-1]) / 1000000
        count = int(frames[-1])
        if abs(duration - seconds) > CLIP_DURATION_TOLERANCE or abs(count - round(seconds * self.fps)) > max(
                2, math.ceil(CLIP_DURATION_TOLERANCE * self.fps)):
            raise RuntimeError("视频片段编码时长或帧数异常：%.3f秒 / %d帧" % (duration, count))
        return True

    def reusable_scene(self, cached, key, clip, duration):
        if (cached.get("passed") is not True or cached.get("key") != key
                or not isinstance(cached.get("duration"), (float, int))
                or abs(cached["duration"] - duration) > 1 / self.fps
                or not isinstance(cached.get("image"), dict)
                or not clip.is_file() or clip.stat().st_size < 2000):
            return False
        voice = cached.get("voice")
        picture = cached["image"]
        if (not voice or not Path(voice).is_file() or audio_seconds(voice) < .15
                or audio_seconds(voice) > duration
                or not picture.get("source") or not Path(picture["source"]).is_file()
                or not cached.get("voice_signature") or not cached.get("visual_signature")
                or file_integrity_hash(voice) != cached["voice_signature"]
                or file_integrity_hash(picture["source"]) != cached["visual_signature"]):
            return False
        layers = picture.get("overlays", [])
        if (not layers or not all(isinstance(item, dict) and Path(item.get("path", "")).is_file()
                                  and full_file_sha256(item["path"]) == item.get("sha256") for item in layers)):
            return False
        try:
            return self.validate_clip(clip, duration)
        except (RuntimeError, OSError, TimeoutError):
            return False

    def choose_size(self):
        aspect = self.request.get("aspect", "横屏 16:9")
        free_ram = memory_info()["available"]
        gpu = gpu_info()
        free_disk = shutil.disk_usage(self.root).free
        if free_ram < 3 * GB or free_disk < 4 * GB:
            side = 512
        elif gpu["free_mb"] >= 9000 and free_ram >= 12 * GB and self.request["quality"] == "精细":
            side = 1280
        elif gpu["free_mb"] >= 5000 and free_ram >= 6 * GB:
            side = 960
        elif free_ram >= 8 * GB:
            side = 768
        else:
            side = 640
        if "竖屏" in aspect:
            return (int(side * 9 / 16) // 2 * 2, side)
        if "方形" in aspect:
            return (side, side)
        return (side, int(side * 9 / 16) // 2 * 2)

    def step(self, message, percent=None):
        if self.resources.resource_stop_reason:
            raise RuntimeError("资源安全保护：" + self.resources.resource_stop_reason)
        if self.cancel.is_set():
            raise InterruptedError("已停止")
        self.notify(message, percent)
        self.log(message)
        sample = self.resources.snapshot(message)
        self.data["events"].append({"at": now_stamp(), "step": message, "percent": percent,
                                    "elapsed_seconds": round(time.monotonic() - self.run_started, 2),
                                    "ram_available": sample["ram_available"],
                                    "gpu_free": sample["gpu_free"],
                                    "disk_free": sample["disk_free"]})
        self.data["resource_report"] = {"peak_ram_pressure": round(self.resources.peak_ram_pressure, 3),
                                        "minimum_available_ram": self.resources.lowest_available_ram,
                                        "minimum_available_gpu": self.resources.lowest_available_gpu}
        if len(self.data["events"]) > 350:
            self.data["events"] = self.data["events"][-300:]
        atomic_json(self.job / "job.json", self.data)

    def gather_inputs(self):
        records = []
        analysis = []
        mandatory = bool(DOCUMENT_REQUIRED_PATTERN.search(self.request.get("prompt", "")))
        unreadable = []
        incomplete = []
        for filename in self.request["files"].get("文档", []):
            self.models.check_stop()
            try:
                content = document_text_controlled(filename, self.root, self.log, self.cancel)
                if content:
                    records.append(("文档 %s" % Path(filename).name, content))
                    coverage = "partial" if len(content) >= MAX_DOCUMENT_TEXT - 256 else "extracted"
                    pages_report = None
                    if Path(filename).suffix.lower() == ".pdf":
                        try:
                            from pypdf import PdfReader
                            with Path(filename).open("rb") as pdf_handle:
                                pdf_pages = len(PdfReader(pdf_handle, strict=False).pages)
                            pages_report = {"total": pdf_pages, "sampled": min(pdf_pages, OCR_PAGES)}
                            if pdf_pages > OCR_PAGES:
                                coverage = "partial"
                        except (OSError, ValueError, ImportError):
                            pages_report = {"status": "count_unavailable"}
                    if coverage == "partial":
                        incomplete.append(Path(filename).name)
                    analysis.append({"kind": "document", "file": Path(filename).name,
                                     "status": coverage, "characters": len(content),
                                     "pdf_pages": pages_report,
                                     "max_characters": MAX_DOCUMENT_TEXT,
                                     "possible_truncation": coverage == "partial"})
                else:
                    analysis.append({"kind": "document", "file": Path(filename).name,
                                     "status": "no_text", "characters": 0})
                    unreadable.append(Path(filename).name)
                    self.warn("文档 %s 没有提取到文字，可能是扫描件或不支持的格式" % Path(filename).name)
            except InterruptedError:
                raise
            except Exception as error:
                analysis.append({"kind": "document", "file": Path(filename).name,
                                 "status": "failed", "failure": str(error)[:180]})
                unreadable.append(Path(filename).name)
                self.warn("文档无法读取或 OCR 不可用，已跳过 %s：%s" % (Path(filename).name, str(error)[:160]))
        if unreadable and mandatory:
            self.data["source_analysis"] = analysis
            atomic_json(self.job / "job.json", self.data)
            raise RuntimeError("提示词明确要求依据附件，但无法读取：" + "、".join(unreadable[:8]) +
                               "。已停止制作，避免生成没有依据的内容")
        if incomplete and mandatory and re.search(r"全文|完整|每一页|全部细节|所有章节", self.request["prompt"]):
            self.data["source_analysis"] = analysis
            atomic_json(self.job / "job.json", self.data)
            raise RuntimeError("用户要求完整依据文档，但内容超过当前安全解析容量：" + "、".join(incomplete[:8]))
        transcript_fields = []
        if self.request.get("audio_role") != "作为背景音乐":
            transcript_fields.append("音频")
        if (self.request.get("source_audio_role") != "静音原声" or
                re.search(r"识别.*(台词|对白|声音)|提取.*(台词|对白|语音)", self.request["prompt"])):
            transcript_fields.append("视频")
        if self.capabilities["speech_review"]:
            selected = [(field, filename) for field in transcript_fields
                        for filename in self.request["files"].get(field, [])]
            for index, (field, filename) in enumerate(selected):
                if index >= MAX_ASR_INPUTS:
                    analysis.append({"kind": field, "file": Path(filename).name, "status": "limit_reached"})
                    continue
                self.models.check_stop()
                try:
                    transcript = self.models.transcribe(filename, self.job, self.log,
                                                        max_seconds=ASR_WINDOW_SECONDS * MAX_ASR_USER_WINDOWS)
                    analysis.append({"kind": field, "file": Path(filename).name,
                                     "status": "speech_recognized" if transcript else "no_speech_detected",
                                     "characters": len(transcript),
                                     "maximum_seconds": ASR_WINDOW_SECONDS * MAX_ASR_USER_WINDOWS})
                    if transcript:
                        records.append(("%s %s 中的声音" % (field, Path(filename).name), transcript))
                except InterruptedError:
                    raise
                except Exception as error:
                    analysis.append({"kind": field, "file": Path(filename).name,
                                     "status": "failed", "failure": str(error)[:180]})
                    self.warn("无法识别 %s 的声音：%s" % (Path(filename).name, str(error)[:130]))
            if len(selected) > MAX_ASR_INPUTS:
                self.warn("音视频语音识别为保护资源最多处理 %d 份，其余仍可用于剪辑" % MAX_ASR_INPUTS)
        elif any(self.request["files"].get(field) for field in transcript_fields):
            self.warn("离线语音识别尚未验收，音视频仍会参与剪辑，但不会声称已理解台词")
        reference = select_reference_snippets(self.request["prompt"], records)
        self.data["source_analysis"] = analysis
        self.data["reference_coverage"] = {"required": mandatory, "failed": unreadable,
                                           "partial": incomplete, "selected_characters": len(reference)}
        self.data["reference_sources"] = [title for title, _ in records]
        self.data["reference_length"] = len(reference)
        atomic_json(self.job / "job.json", self.data)
        return reference

    def create_speech(self, text, stem):
        path = self.job / (stem + ".txt")
        ps1 = self.job / (stem + ".ps1")
        output = self.job / (stem + "_sapi.wav")
        piper_output = self.job / (stem + "_piper.wav")
        normalized = self.job / (stem + ".wav")
        path.write_text(text, encoding="utf-8-sig")
        backends = [self.voice_backend, "sapi" if self.voice_backend == "piper" else "piper"]
        failures = []
        for backend in backends:
            if backend == "piper" and not voice_model_ready(self.root):
                continue
            try:
                if backend == "piper":
                    try:
                        if self.piper_worker is None:
                            self.piper_worker = PersistentPiper(self.root, self.cancel, self.log)
                        self.piper_worker.synthesize(path, piper_output)
                    except InterruptedError:
                        raise
                    except Exception as server_error:
                        self.log("常驻语音引擎不可用，切换单次离线合成：" + str(server_error)[:200])
                        if self.piper_worker is not None:
                            self.piper_worker.close()
                            self.piper_worker = None
                        run_external([str(runtime_python(self.root)), str(Path(__file__).resolve()),
                                      "--speak", str(self.root), str(path), str(piper_output)],
                                     self.root, cancel=self.cancel, timeout=MAX_SPEECH_RESPONSE_SECONDS,
                                     log=self.log, capture=True, env=shell_env(self.root, offline=True))
                    source = piper_output
                else:
                    output_ps = str(output).replace("'", "''")
                    input_ps = str(path).replace("'", "''")
                    ps1.write_text("Add-Type -AssemblyName System.Speech\n"
                                   "$voice=New-Object System.Speech.Synthesis.SpeechSynthesizer\n"
                                   "$choices=@($voice.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like 'zh*' })\n"
                                   "if ($choices.Count -eq 0) { throw '系统缺少中文离线语音' }\n"
                                   "$voice.SelectVoice($choices[0].VoiceInfo.Name)\n"
                                   "$voice.Rate=1\n"
                                   "$voice.SetOutputToWaveFile('" + output_ps + "')\n"
                                   "$voice.Speak([System.IO.File]::ReadAllText('" + input_ps +
                                   "',[System.Text.Encoding]::UTF8))\n"
                                   "$voice.Dispose()\n", encoding="utf-8-sig")
                    run_external(["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
                                  "-File", str(ps1)], self.root, log=self.log, cancel=self.cancel,
                                 timeout=90, capture=True)
                    source = output
                normalized_wave(source, normalized, self.root, self.log, duration=None, cancel=self.cancel)
                if audio_seconds(normalized) < .15:
                    raise RuntimeError("合成结果没有有效的语音时长")
                return normalized
            except InterruptedError:
                raise
            except Exception as error:
                failures.append("%s: %s" % (backend, str(error)[:200]))
                self.log("离线中文旁白尝试失败：" + failures[-1])
        raise RuntimeError("中文旁白生成失败，请通过黑匣子检查语音组件：" + "；".join(failures))

    def review_native_video(self, source, scene, index):
        metadata = read_json(str(source) + ".json", {})
        seconds = float(metadata.get("seconds", NATIVE_VIDEO_FRAMES / NATIVE_VIDEO_FPS))
        if seconds < 1 or not Path(source).is_file():
            raise RuntimeError("原生视频输出时长或文件异常")
        measurements = []
        stills = []
        for number, fraction in enumerate(NATIVE_REVIEW_FRACTIONS):
            self.models.check_stop()
            still = self.job / ("native_review_%02d_%d.png" % (index, number))
            extract_video_frame(self.ffmpeg, source, still,
                                max(0, (seconds - 1 / NATIVE_VIDEO_FPS) * fraction),
                                self.root, cancel=self.cancel, log=self.log)
            valid, reason = validate_image(still)
            if not valid:
                raise RuntimeError("原生视频关键帧%d异常：%s" % (number + 1, reason))
            check = self.models.image_similarity(still, scene["visual_prompt"])
            stills.append(still)
            measurements.append({"position": round(seconds * fraction, 3), **check})
        temporal = [round(image_mean_difference(first, second), 3)
                    for first, second in zip(stills, stills[1:])]
        motion_ok = (len(stills) >= MIN_MOTION_REVIEW_FRAMES and
                     max(temporal, default=0) >= MIN_NATIVE_TEMPORAL_DIFFERENCE and
                     all(value <= MAX_NATIVE_TEMPORAL_DIFFERENCE for value in temporal))
        seams = []
        for number, (before, after) in enumerate(native_seam_positions(metadata)):
            self.models.check_stop()
            positions = [max(0, before - 1 / NATIVE_VIDEO_FPS), before, after,
                         min(seconds - 1 / NATIVE_VIDEO_FPS, after + 1 / NATIVE_VIDEO_FPS)]
            paths = []
            for offset, position in enumerate(positions):
                still = self.job / ("native_seam_%02d_%02d_%d.png" % (index, number, offset))
                extract_video_frame(self.ffmpeg, source, still, position, self.root,
                                    cancel=self.cancel, log=self.log)
                valid, reason = validate_image(still, allow_flat=True)
                if not valid:
                    raise RuntimeError("原生视频拼接处无效：" + reason)
                paths.append(still)
            normal_left = image_mean_difference(paths[0], paths[1])
            jump = image_mean_difference(paths[1], paths[2])
            normal_right = image_mean_difference(paths[2], paths[3])
            limit = max(NATIVE_SEAM_DIFFERENCE_MAX, max(normal_left, normal_right) * 2.25 + 12)
            seams.append({"time": round(after, 4), "difference": round(jump, 3),
                          "neighbor_differences": [round(normal_left, 3), round(normal_right, 3)],
                          "limit": round(limit, 3), "passed": jump <= limit})
        seams_ok = all(item["passed"] for item in seams)
        required_matches = max(2, math.ceil(len(measurements) * .70))
        passed = (motion_ok and seams_ok and
                  sum(bool(item["passed"]) for item in measurements) >= required_matches and
                  sum(item["cosine"] for item in measurements) / len(measurements) >=
                  sum(item["required_cosine"] for item in measurements) / len(measurements) and
                  sum(item["margin"] for item in measurements) / len(measurements) >=
                  sum(item["required_margin"] for item in measurements) / len(measurements))
        return {"passed": passed, "cosine": round(sum(v["cosine"] for v in measurements) /
                                                  len(measurements), 4),
                "margin": round(sum(v["margin"] for v in measurements) / len(measurements), 4),
                "keyframes": measurements, "seconds": seconds,
                "temporal_differences": temporal, "temporal_review_passed": motion_ok,
                "seam_reviews": seams, "seam_review_passed": seams_ok,
                "review_method": "CLIP sampled frames plus grayscale temporal/seam heuristics"}

    def review_supplied_visual(self, path, scene, index, kind="image", obligated=False):
        path = Path(path)
        samples = [path]
        if kind == "video":
            samples = []
            for number, stamp in enumerate((0.0, .7, 1.8)):
                self.models.check_stop()
                filename = self.job / ("asset_review_%02d_%d.png" % (index, number))
                try:
                    run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                                  "-ss", "%.3f" % stamp, "-i", str(path), "-frames:v", "1",
                                  "-vf", "scale='min(480,iw)':-2", str(filename)],
                                 self.root, log=self.log, cancel=self.cancel, timeout=90, capture=True)
                    okay, _ = validate_image(filename, allow_flat=True)
                    if okay:
                        samples.append(filename)
                except InterruptedError:
                    raise
                except (RuntimeError, OSError, ValueError, TimeoutError):
                    continue
        if not samples:
            return {**visual_review_record(False, None, False, supplied=True, reason="素材无法提取有效画面"),
                    "samples": [], "kind": kind}
        quality = []
        for candidate in samples:
            valid, detail = validate_image(candidate, allow_flat=True)
            if not valid:
                return {**visual_review_record(False, None, False, supplied=True, reason=detail),
                        "samples": [str(item) for item in samples], "kind": kind}
            if self.capabilities["semantic_review"]:
                quality.append(self.models.image_similarity(candidate, scene["visual_prompt"]))
        semantic = None
        if quality:
            cosine = sum(float(item["cosine"]) for item in quality) / len(quality)
            margin = sum(float(item["margin"]) for item in quality) / len(quality)
            required_cosine = sum(float(item["required_cosine"]) for item in quality) / len(quality)
            required_margin = sum(float(item["required_margin"]) for item in quality) / len(quality)
            accepted_count = sum(item["passed"] for item in quality)
            accepted = (accepted_count >= math.ceil(len(quality) * .67) and
                        cosine >= required_cosine and margin >= required_margin)
            semantic = {"cosine": round(cosine, 4), "margin": round(margin, 4),
                        "required_cosine": round(required_cosine, 4),
                        "required_margin": round(required_margin, 4),
                        "samples_passed": accepted_count, "sample_count": len(quality),
                        "passed": bool(accepted),
                        "method": "CLIP 多帧正负锚点比较；不能核实动作、数量或身份事实"}
        record = visual_review_record(True, semantic, True, supplied=True,
                                     reason="用户指定素材优先保留" if obligated else "素材已通过技术解码检查")
        record.update({"samples": [str(item) for item in samples], "kind": kind,
                       "cosine": semantic.get("cosine") if semantic else None,
                       "margin": semantic.get("margin") if semantic else None,
                       "sample_reviews": quality, "obligated": bool(obligated)})
        if record["semantic_passed"] is False:
            self.data["review_summary"]["user_semantic_warning"] += 1
            self.warn("第 %d 幕用户素材与分镜语义评分偏低；已保留原素材，并标注未通过语义审校" % (index + 1))
        elif record["semantic_passed"] is None:
            self.data["review_summary"]["not_checked"] += 1
            self.warn("第 %d 幕素材仅完成技术检查；离线语义审校尚未验收" % (index + 1))
        else:
            self.data["review_summary"]["approved"] += 1
        self.publish_event("scene_review", index=index, total=len(self.active_plan["scenes"]),
                           state=record["review_status"], review=record["reason"])
        return record

    def prepare_native_videos(self, contexts, repair_round):
        prepared = {}
        model = native_video_model(self.root)
        if not self.request.get("visual_mode", "").startswith("原生AI视频") or model is None:
            return prepared
        image_mode = model[1] == "CogVideoXImageToVideoPipeline"
        self.models.unload_director()
        for context in contexts:
            if context["cached"] or context.get("reuse_visual"):
                continue
            selected = context["selected"]
            boundary = (context["index"] == 0 and self.request["files"].get("首帧") or
                        context["index"] == len(contexts) - 1 and self.request["files"].get("尾帧"))
            if selected and (not image_mode or selected[0] != "image" or boundary):
                continue
            if not image_mode and context["length"] > NATIVE_VIDEO_FRAMES / NATIVE_VIDEO_FPS:
                self.log("当前文生视频模型不足以覆盖整幕时长，改为经审校的图片运镜")
                continue
            index = context["index"]
            scene = context["scene"]
            prompt = scene["visual_prompt"]
            attempts = []
            for attempt in range(MAX_NATIVE_ATTEMPTS):
                self.models.check_stop()
                self.step("第 %d 幕 · 原生视频生成与关键帧审校" % (index + 1), 38)
                output = self.job / ("native_%02d_%d_%d.mp4" % (index, repair_round, attempt))
                prompt_file = self.job / ("native_prompt_%02d.txt" % index)
                prompt_file.write_text(prompt, encoding="utf-8")
                try:
                    self.resources.ensure("native_video", disk_required=MIN_JOB_FREE)
                    reference = None
                    if image_mode:
                        if selected:
                            reference = selected[1]
                        else:
                            reference = str(self.job / ("native_reference_%02d.png" % index))
                            if not Path(reference).is_file():
                                self.models.paint(scene["visual_prompt"], reference,
                                                  int(hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8], 16),
                                                  "快速", self.request["aspect"])
                            self.models.unload_painter()
                    args = [str(runtime_python(self.root)), str(Path(__file__).resolve()),
                            "--render-native", str(self.root), str(prompt_file), str(output),
                            self.request["quality"], str(context["length"])]
                    args.extend([str(reference) if reference else "", self.request["aspect"]])
                    run_external(args, self.root, log=self.log, cancel=self.cancel,
                                 timeout=2700, env=shell_env(self.root, offline=True))
                    review = self.review_native_video(output, scene, index)
                    attempts.append({"prompt": prompt, "review": review,
                                     "repair_type": review_failure_type(review) if not review["passed"] else None})
                    if review["passed"]:
                        preview = self.job / ("native_preview_%02d.png" % index)
                        shutil.copy2(self.job / ("native_review_%02d_1.png" % index), preview)
                        prepared[index] = {"type": "native_video", "source": str(output),
                                           "thumbnail": str(preview),
                                           "metrics": {**review, **visual_review_record(True, review)},
                                           "review": "原生视频多关键帧 AI 审校通过", "render_method": "cogvideox_generated_motion",
                                           "attempts": attempts,
                                           "source_seconds": review["seconds"]}
                        break
                    prompt = self.models.refine_visual(scene["visual_prompt"], review, attempt,
                                                       self.request["prompt"])
                except InterruptedError:
                    raise
                except (OSError, ValueError, RuntimeError, MemoryError, TimeoutError) as error:
                    attempts.append({"prompt": prompt, "failure": str(error)[:400],
                                     "repair_type": "memory" if is_memory_error(error) else "generation_failed"})
                    self.log("第 %d 幕原生视频未通过：%s" % (index + 1, str(error)[:260]))
                    if is_memory_error(error):
                        break
                    prompt = refine_visual_prompt(scene["visual_prompt"], None, attempt,
                                                  self.request["prompt"])
            if index not in prepared:
                self.warn("第 %d 幕原生视频未通过审校，将尝试经审校的图片运镜作为明确标注的替代方案" % (index + 1))
            atomic_json(self.job / ("native_attempts_%02d.json" % index), attempts)
        return prepared

    def prepare_generated_images(self, contexts, force_scenes, repair_round, native_prepared=None):
        pending = {}
        prepared = {}
        native_prepared = native_prepared or {}
        for context in contexts:
            index = context["index"]
            if context["cached"] or context.get("reuse_visual") or context["selected"] or index in native_prepared:
                continue
            snapshot = self.job / ("approved_%02d.json" % index)
            recorded = read_json(snapshot, {})
            image = self.job / ("shot_%02d.png" % index)
            if (index not in force_scenes and recorded.get("key") == context["key"]
                    and recorded.get("review", {}).get("passed") is True and image.is_file()):
                okay, _ = validate_image(image)
                if okay:
                    prepared[index] = {"type": "image", "source": str(image), "review": "恢复已通过的画面",
                                       "metrics": recorded["review"], "render_method": "generated_still_camera_motion",
                                       "attempts": recorded.get("attempts", [])}
                    continue
            pending[index] = {"context": context, "prompt": context["scene"]["visual_prompt"],
                              "attempts": [], "candidate": None}
        for attempt in range(MAX_SCENE_ATTEMPTS):
            if not pending:
                break
            self.step("批量生成画面 %d/%d · 待处理 %d 幕" % (
                attempt + 1, MAX_SCENE_ATTEMPTS, len(pending)),
                38 + int((attempt / MAX_SCENE_ATTEMPTS) * 20))
            for index, item in pending.items():
                self.models.check_stop()
                seed_text = "%s:%s:%s:%s" % (self.request["prompt"], index, attempt, repair_round)
                seed = int(hashlib.sha256(seed_text.encode("utf-8")).hexdigest()[:8], 16)
                candidate = self.job / ("candidate_%02d_%d_%d.png" % (index, repair_round, attempt))
                item["candidate"] = None
                try:
                    consistent = (" Consistent visual style and character identity across all shots, "
                              "harmonized cinematic color palette, realistic composition. ")
                    self.models.paint(item["prompt"] + consistent, candidate, seed,
                                      self.request["quality"], self.request["aspect"])
                    valid, reason = validate_image(candidate)
                    if valid:
                        item["candidate"] = candidate
                    else:
                        item["attempts"].append({"prompt": item["prompt"], "failure": reason})
                        item["prompt"] = refine_visual_prompt(item["context"]["scene"]["visual_prompt"],
                                                              None, attempt, self.request["prompt"])
                except InterruptedError:
                    raise
                except (OSError, ValueError, RuntimeError, MemoryError) as error:
                    item["attempts"].append({"prompt": item["prompt"], "error": str(error)[:500]})
                    self.log("第 %d 幕画面生成失败：%s" % (index + 1, str(error)[:260]))
            self.models.unload_painter()
            for index, item in list(pending.items()):
                candidate = item["candidate"]
                if candidate is None:
                    continue
                try:
                    review = self.models.image_similarity(candidate, item["context"]["scene"]["visual_prompt"])
                except InterruptedError:
                    raise
                except (OSError, ValueError, RuntimeError, MemoryError) as error:
                    raise RuntimeError("第 %d 幕 AI 语义审校失败，不能冒充已通过：%s" % (
                        index + 1, str(error)[:300])) from error
                anchors = visual_constraints(item["context"]["scene"]["visual_prompt"])
                retained = visual_constraints_retained(item["prompt"], anchors)
                review["constraint_text_preserved"] = retained
                review["explicit_constraints"] = anchors[:16]
                review["verification_limits"] = "不能仅凭 CLIP 验证准确数量、特定身份或真实动作"
                review["passed"] = bool(review["passed"] and retained)
                item["attempts"].append({"prompt": item["prompt"], "review": review})
                self.log("第 %d 幕语义审校：相似度 %.3f、相对差值 %.3f · %s" % (
                    index + 1, review["cosine"], review["margin"],
                    "通过" if review["passed"] else "等待自动修复"))
                if review["passed"]:
                    shot = self.job / ("shot_%02d.png" % index)
                    shutil.copy2(candidate, shot)
                    prepared[index] = {"type": "image", "source": str(shot), "review": "本地 AI 语义审校通过",
                                       "metrics": {**review, **visual_review_record(True, review)},
                                       "render_method": "generated_still_camera_motion",
                                       "attempts": item["attempts"]}
                    atomic_json(self.job / ("approved_%02d.json" % index),
                                {"key": item["context"]["key"], "review": review,
                                 "attempts": item["attempts"], "time": now_stamp()})
                    del pending[index]
                else:
                    item["prompt"] = self.models.refine_visual(
                        item["context"]["scene"]["visual_prompt"], review, attempt,
                        self.request["prompt"])
                    item["attempts"][-1]["repair_type"] = review_failure_type(review)
                    item["attempts"][-1]["next_prompt"] = item["prompt"]
            if pending and memory_info()["available"] < MODEL_SWITCH_FREE_BYTES:
                self.models.unload_inspector()
        if pending:
            summaries = []
            for index, item in pending.items():
                atomic_json(self.job / ("attempts_%02d.json" % index), item["attempts"])
                summaries.append("第 %d 幕：%s" % (index + 1, str(item["attempts"][-1:])[:250]))
            raise RuntimeError("自动重新生成后仍有画面未通过 AI 审校：" + "；".join(summaries))
        self.models.unload_painter()
        return prepared

    def compose_clips(self, plan, force_scenes=None, repair_round=0, preserve_visual=None):
        scenes = plan["scenes"]
        previous_timeline = [scene.get("seconds") for scene in scenes]
        if all(isinstance(value, (int, float)) and value >= 2 for value in previous_timeline) and (
                abs(sum(previous_timeline) - self.request["duration"]) <= 1 / self.fps):
            timeline = [float(value) for value in previous_timeline]
        else:
            timeline = semantic_timeline(self.request["duration"], scenes, self.fps)
        self.active_plan = plan
        assignments = self.assign_assets(scenes)
        force_scenes = set(force_scenes or [])
        preserve_visual = set(preserve_visual or [])
        contexts = []
        for index, scene in enumerate(scenes):
            self.models.check_stop()
            clip = self.job / ("clip_%02d.mp4" % index)
            checkpoint_file = self.job / ("scene_%02d.json" % index)
            cached = read_json(checkpoint_file, {})
            length = timeline[index]
            selected = assignments.get(index)
            extras = self.scene_extra_assets.get(index, [])
            extras_signature = hashlib.sha256(json.dumps(
                [(kind, file_integrity_hash(path)) for kind, path in extras], ensure_ascii=False
            ).encode("utf-8")).hexdigest() if extras else ""
            key_signature = self.cache_signature + ":" + extras_signature
            key = scene_cache_key(scene, length, self.request["aspect"], self.request["quality"],
                                  selected, self.size, self.fps, key_signature)
            reuse = index not in force_scenes and self.reusable_scene(cached, key, clip, length)
            saved_visual = cached.get("image") if index in preserve_visual and cached.get("passed") else None
            if saved_visual and (not isinstance(saved_visual, dict) or
                                 not Path(saved_visual.get("source", "")).is_file() or
                                 not cached.get("visual_signature") or
                                 file_integrity_hash(saved_visual["source"]) != cached["visual_signature"]):
                saved_visual = None
            if reuse:
                self.log("第 %d 幕已通过编码检查，可直接恢复" % (index + 1))
                track = Path(cached["voice"])
            else:
                self.step("第 %d/%d 幕 · 准备中文旁白" % (index + 1, len(scenes)),
                          22 + int(index / len(scenes) * 15))
                track = self.fit_speech(scene, "speech_%02d" % index, length)
                key = scene_cache_key(scene, length, self.request["aspect"], self.request["quality"],
                                      selected, self.size, self.fps, key_signature)
                atomic_json(self.job / "storyboard.json", plan)
            contexts.append({"index": index, "scene": scene, "clip": clip, "checkpoint": checkpoint_file,
                             "cached": cached if reuse else None, "length": length, "selected": selected,
                             "reuse_visual": saved_visual, "key": key, "track": track,
                             "extras": extras})
        if not self.capabilities["image_generation"]:
            missing = [context["index"] + 1 for context in contexts if
                       not context["cached"] and not context["selected"] and not context.get("reuse_visual")]
            if missing:
                raise RuntimeError("以下镜头没有素材且离线生图尚未就绪：" + ", ".join(map(str, missing)))
        self.models.unload_director()
        native_prepared = self.prepare_native_videos(contexts, repair_round)
        self.step("集中生成和检查需要的画面", 38)
        prepared = self.prepare_generated_images(contexts, force_scenes, repair_round, native_prepared)
        clips, wavs, images, original_videos = [], [], [], []
        for context in contexts:
            index, scene, clip = context["index"], context["scene"], context["clip"]
            length, selected, track = context["length"], context["selected"], context["track"]
            self.publish_event("scene_active", index=index, total=len(scenes))
            if context["cached"]:
                visual = context["cached"]["image"]
            else:
                framefile = self.job / ("shot_%02d.png" % index)
                title = plan["title"] if index == 0 else ""
                original_video = selected[1] if selected and selected[0] == "video" else None
                base = selected[1] if selected and selected[0] == "image" else None
                reused_visual = context.get("reuse_visual")
                if reused_visual:
                    if reused_visual.get("type") in {"native_video", "video"}:
                        if index in self.motion_safe_scenes and reused_visual.get("type") == "native_video":
                            base = reused_visual.get("thumbnail")
                            original_video = None
                        else:
                            original_video = reused_visual["source"]
                    elif reused_visual.get("type") == "image":
                        base = reused_visual["source"]
                boundary_image = bool(base and (
                    (index == 0 and self.request["files"].get("首帧")) or
                    (index == len(scenes) - 1 and self.request["files"].get("尾帧"))))
                if index in native_prepared:
                    visual = dict(native_prepared[index])
                    original_video = visual["source"]
                    clipsrc = original_video
                elif original_video:
                    clipsrc = original_video
                    visual = dict(reused_visual) if reused_visual else {
                        "type": "video", "source": str(original_video),
                        "review": "已采用用户视频，并执行逐帧与语义检查",
                        "render_method": "supplied_video_edit"}
                    if not reused_visual:
                        visual["metrics"] = self.review_supplied_visual(
                            original_video, scene, index, kind="video")
                        if not visual["metrics"]["technical_passed"]:
                            raise RuntimeError("第 %d 幕用户视频无法解码，拒绝以无效素材继续" % (index + 1))
                    thumbnail = self.job / ("preview_%02d.png" % index)
                    try:
                        png_or_video_image(original_video, thumbnail, self.root, self.log, cancel=self.cancel)
                        visual["thumbnail"] = str(thumbnail)
                    except (OSError, RuntimeError, TimeoutError) as error:
                        self.log("视频预览不可用：" + str(error)[:200])
                else:
                    if base:
                        from PIL import Image, ImageOps
                        if Path(base).resolve() != framefile.resolve():
                            with Image.open(base) as source_image:
                                source_image.draft("RGB", (max(self.size) * 2, max(self.size) * 2))
                                source_image.thumbnail((max(self.size) * 2, max(self.size) * 2), Image.Resampling.LANCZOS)
                                picture = ImageOps.exif_transpose(source_image).convert("RGB")
                                picture.save(framefile)
                        visual = dict(reused_visual) if reused_visual else {
                            "type": "image", "source": str(framefile), "review": "采用用户提供的画面", "render_method": "supplied_still_camera_motion"}
                        if index in self.motion_safe_scenes and visual.get("type") == "native_video":
                            visual.update({"type": "image", "source": str(framefile),
                                           "review": "原生动态画面闪烁，保留已审核关键帧改为安全静态镜头",
                                           "source_seconds": None})
                        if not reused_visual:
                            visual["metrics"] = self.review_supplied_visual(
                                framefile, scene, index, kind="image", obligated=boundary_image)
                            if not visual["metrics"]["technical_passed"]:
                                raise RuntimeError("第 %d 幕用户图片技术检查失败" % (index + 1))
                    else:
                        visual = prepared[index]
                    rendered = self.job / ("caption_%02d.png" % index)
                    frame_with_caption(framefile, rendered, self.size, "", "")
                    valid, reason = validate_image(rendered, allow_flat=bool(base))
                    if not valid:
                        raise RuntimeError("第 %d 幕字幕合成后图片检查失败：%s" % (index + 1, reason))
                    visual["rendered"] = str(rendered)
                    clipsrc = rendered
                overlays = self.build_caption_overlays(index, scene["narration"], length, title,
                    boundary_first=boundary_image and index == 0,
                    boundary_last=boundary_image and index == len(scenes) - 1)
                visual["overlays"] = overlays
                visual["caption_mask"] = overlays[0]["path"] if overlays else None
                montage = self.encode_scene_montage(
                    clip, clipsrc, original_video, length, overlays, index, len(scenes), selected,
                    context.get("extras", []),
                    native_seconds=visual.get("source_seconds") if visual.get("type") == "native_video" else None,
                    boundary_image=boundary_image)
                if montage:
                    visual["montage"] = montage
                atomic_json(context["checkpoint"], {"passed": True, "duration": length,
                            "key": context["key"], "voice": str(track), "image": visual,
                            "voice_signature": file_integrity_hash(track),
                            "visual_signature": file_integrity_hash(visual["source"]),
                            "clip": str(clip), "time": now_stamp()})
            clips.append(clip)
            wavs.append(str(track))
            images.append(visual)
            montage = visual.get("montage", [])
            original_videos.append(montage if montage else
                                   ([{"kind": "video", "source": selected[1], "seconds": length}]
                                    if selected and selected[0] == "video" else []))
            metrics = visual.get("metrics", {})
            status = metrics.get("review_status", "unreviewed") if isinstance(metrics, dict) else "unreviewed"
            self.publish_event("scene_ready", index=index, total=len(scenes),
                               preview=visual.get("rendered") or visual.get("thumbnail") or
                               (visual.get("source") if visual.get("type") == "image" else ""),
                               review=visual.get("review", "检查已完成") + " · " + status)
            self.step("第 %d/%d 幕已完成，可断点恢复" % (index + 1, len(scenes)),
                      60 + int((index + 1) / len(scenes) * 20))
        voice = self.job / "voice.wav"
        join_voice_audio(wavs, timeline, voice)
        self.write_subtitle_timeline(scenes, timeline, wavs)
        self.original_videos = original_videos
        return clips, voice, sum(timeline), images

    def encode_scene_montage(self, clip, clipsrc, original_video, seconds, overlays, index,
                             scene_count, primary, extras, native_seconds=None, boundary_image=False):
        effective_primary = primary or ("video" if original_video else "image", str(original_video or clipsrc))
        sequence = asset_sequence_for_scene(effective_primary, extras, index, scene_count, self.request)
        if len(sequence) <= 1:
            self.encode_clip(clip, clipsrc, original_video, seconds, overlays,
                             first=index == 0, last=index == scene_count - 1,
                             native_seconds=native_seconds,
                             boundary_hold=boundary_image or index in self.motion_safe_scenes)
            return [{"kind": effective_primary[0], "source": str(effective_primary[1]),
                     "seconds": seconds, "primary": True}]
        durations = montage_frame_allocation(seconds, sequence, self.fps)
        parts = []
        records = []
        for slot, ((kind, path), length) in enumerate(zip(sequence, durations)):
            is_primary = bool(kind == effective_primary[0] and path == effective_primary[1])
            actual_source = (original_video or clipsrc) if is_primary else str(path)
            video = actual_source if (kind == "video" or is_primary and original_video) else None
            if is_primary and not video:
                actual_source = clipsrc
            if not is_primary:
                evaluation = self.review_supplied_visual(path, self.active_plan["scenes"][index], index, kind)
                if not evaluation.get("technical_passed"):
                    raise RuntimeError("额外素材无法解码：" + Path(path).name)
            part_file = self.job / ("scene_%02d_visual_%02d.mp4" % (index, slot))
            self.encode_clip(part_file, actual_source, video, length, first=True, last=True,
                             native_seconds=native_seconds if is_primary and video and
                             native_seconds is not None and native_seconds >= length else None,
                             boundary_hold=(boundary_image and is_primary or index in self.motion_safe_scenes))
            parts.append(part_file)
            records.append({"kind": kind, "source": str(path), "seconds": length,
                            "segment": str(part_file), "primary": is_primary})
        assembled = self.job / ("scene_%02d_montage.mp4" % index)
        self.concat_clips(parts, assembled)
        self.encode_clip(clip, assembled, assembled, seconds, overlays,
                         first=index == 0, last=index == scene_count - 1)
        return records


    def build_caption_overlays(self, index, text, seconds, title="", boundary_first=False, boundary_last=False):
        segments = paginate_caption(text, self.size, seconds, self.fps)
        overlays = []
        for page_index, segment in enumerate(segments):
            output = self.job / ("overlay_%02d_%02d.png" % (index, page_index))
            frame_with_caption(None, output, self.size, segment["text"],
                               title if page_index == 0 else "", transparent=True)
            start = max(segment["start"], FIRST_LAST_HOLD_SECONDS if boundary_first else 0)
            end = min(segment["end"], seconds - FIRST_LAST_HOLD_SECONDS if boundary_last else seconds)
            if end - start <= 1 / self.fps:
                raise ValueError("镜头 %d 的字幕显示时段过短，无法保证全部文字可读" % (index + 1))
            overlays.append({"path": str(output), "start": round(start, 6), "end": round(end, 6),
                             "text": segment["text"], "sha256": full_file_sha256(output)})
        if normalized_caption("".join(item["text"] for item in overlays)) != normalized_caption(text):
            raise RuntimeError("字幕页未完整覆盖旁白，禁止输出被截断的成片")
        return overlays

    def write_subtitle_timeline(self, scenes, durations, wavs):
        cursor = 0.0
        subtitles = []
        for index, (scene, duration) in enumerate(zip(scenes, durations)):
            info = read_json(self.job / ("scene_%02d.json" % index), {})
            segments = info.get("image", {}).get("overlays", [])
            if not segments or normalized_caption("".join(part["text"] for part in segments)) != normalized_caption(scene["narration"]):
                raise RuntimeError("第 %d 幕没有完整的分段字幕记录" % (index + 1))
            subtitles.append({"index": index, "from": round(cursor, 5),
                              "to": round(cursor + duration, 5), "caption": scene["narration"],
                              "segments": segments, "voice_file": str(wavs[index]),
                              "voice_sha256": file_integrity_hash(wavs[index]),
                              "voice_seconds": round(audio_seconds(wavs[index]), 3)})
            cursor += duration
        atomic_json(self.job / "subtitle_timeline.json", subtitles)
        return subtitles

    def encode_clip(self, clip, source, source_video, seconds, overlay=None, first=False, last=False,
                    native_seconds=None, boundary_hold=False):
        width, height = self.size
        fade = min(.28, seconds / 10)
        effects = []
        if not first:
            effects.append("fade=t=in:st=0:d=%.2f" % fade)
        if not last:
            effects.append("fade=t=out:st=%.3f:d=%.2f" % (max(.1, seconds - fade), fade))
        effects.append("format=yuv420p")
        effects = ",".join(effects)
        common = ["-threads", str(available_threads()), "-c:v", "libx264", "-preset", "veryfast",
                  "-crf", "24", "-pix_fmt", "yuv420p", "-r", str(self.fps), "-an", "-movflags", "+faststart"]
        args = [self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
        if source_video:
            if native_seconds is not None and "竖屏" in self.request.get("aspect", ""):
                filters = ["scale=%d:%d:force_original_aspect_ratio=decrease" % (width, height),
                           "pad=%d:%d:(ow-iw)/2:(oh-ih)/2:color=0x0d1727" % (width, height), "setsar=1"]
            else:
                filters = ["scale=%d:%d:force_original_aspect_ratio=increase" % (width, height),
                           "crop=%d:%d" % (width, height), "setsar=1"]
            if native_seconds is not None:
                source_length = max(.1, float(native_seconds))
                if source_length < seconds / NATIVE_VIDEO_MAX_SLOWDOWN:
                    raise RuntimeError("原生视频真实动态时长不足；不通过复制静止末帧伪装动态")
                stretch = seconds / source_length
                filters.append("setpts=%.6f*(PTS-STARTPTS)" % stretch)
                filters.append("fps=%d" % self.fps)
            else:
                filters.append("fps=%d" % self.fps)
            if native_seconds is None:
                args.extend(["-stream_loop", "-1"])
            args += ["-i", str(source_video)]
            visual = ",".join(filters + [effects])
        else:
            args += ["-loop", "1", "-framerate", str(self.fps), "-i", str(source)]
            zoomstep = max(.00015, .09 / max(1, seconds * self.fps))
            visual = ("scale=%d:%d:force_original_aspect_ratio=increase,crop=%d:%d,"
                      "zoompan=z='min(zoom+%.6f,1.09)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                      "d=1:s=%dx%d:fps=%d") % (width, height, width, height, zoomstep,
                                                 width, height, self.fps)
            if boundary_hold:
                visual = "scale=%d:%d,setsar=1,fps=%d" % (width, height, self.fps)
            visual += "," + effects
        layers = overlay if isinstance(overlay, list) else ([{"path": str(overlay), "start": 0, "end": seconds}]
                                                              if overlay else [])
        if layers:
            filters = ["[0:v]" + visual + "[background]"]
            previous = "background"
            for number, part in enumerate(layers, 1):
                args.extend(["-loop", "1", "-framerate", str(self.fps), "-i", str(part["path"])])
                following = "v" if number == len(layers) else "layer%d" % number
                last_frame = max(part["start"], part["end"] - CAPTION_SEGMENT_GAP_FRAMES / self.fps)
                filters.append("[%s][%d:v]overlay=0:0:shortest=1:enable='between(t,%.5f,%.5f)'[%s]" %
                               (previous, number, part["start"], last_frame, following))
                previous = following
            args += ["-filter_complex", ";".join(filters), "-map", "[v]"]
        else:
            args += ["-vf", visual]
        args += ["-t", "%.5f" % seconds] + common + [str(clip)]
        run_external(args, self.root, log=self.log, cancel=self.cancel,
                     timeout=max(240, int(seconds * 30)), capture=True)
        self.validate_clip(clip, seconds)

    def concat_clips(self, clips, output):
        concat_path = self.job / "concat.txt"
        concat_path.write_text("\n".join("file '%s'" % str(path).replace("\\", "/").replace("'", "'\\''")
                                          for path in clips), encoding="utf-8")
        run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0",
                      "-i", str(concat_path), "-c", "copy", str(output)], self.root, log=self.log,
                     cancel=self.cancel, timeout=300, capture=True)
        if output.stat().st_size < 2000:
            raise RuntimeError("片段合并失败")

    def build_original_audio(self, durations):
        videos = getattr(self, "original_videos", [])
        if (self.request.get("source_audio_role", "自动混合原声") == "静音原声"
                or not any(any(item.get("kind") == "video" for item in group)
                           if isinstance(group, list) else bool(group) for group in videos)):
            return None
        destination = self.job / "original_audio.wav"
        sound_count = 0
        with wave.open(str(destination), "wb") as writer:
            writer.setnchannels(1)
            writer.setsampwidth(2)
            writer.setframerate(SPEECH_RATE)
            for index, seconds in enumerate(durations):
                self.models.check_stop()
                expected = round(seconds * SPEECH_RATE)
                track = self.job / ("source_audio_%02d.wav" % index)
                raw = b""
                source = videos[index] if index < len(videos) else []
                segments = source if isinstance(source, list) else (
                    [{"kind": "video", "source": source, "seconds": seconds}] if source else [])
                copied = 0
                for slot, segment in enumerate(segments):
                    length = max(0.0, float(segment.get("seconds", 0)))
                    frame_count = min(max(0, expected - copied), round(length * SPEECH_RATE))
                    if not frame_count:
                        continue
                    part = bytes(frame_count * 2)
                    if segment.get("kind") == "video":
                        track = self.job / ("source_audio_%02d_%02d.wav" % (index, slot))
                        try:
                            run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y",
                                          "-stream_loop", "-1", "-i", str(segment["source"]), "-map", "0:a:0?",
                                          "-vn", "-t", "%.6f" % length, "-ar", str(SPEECH_RATE),
                                          "-ac", "1", "-c:a", "pcm_s16le", str(track)],
                                         self.root, log=self.log, cancel=self.cancel,
                                         timeout=max(FFMPEG_INPUT_TIMEOUT, int(length * 18)), capture=True)
                            if track.is_file():
                                with wave.open(str(track), "rb") as reader:
                                    if (reader.getnchannels() == 1 and reader.getsampwidth() == 2 and
                                            reader.getframerate() == SPEECH_RATE):
                                        data = reader.readframes(frame_count)[:frame_count * 2]
                                        part = data + bytes(max(0, frame_count * 2 - len(data)))
                                        if data:
                                            sound_count += 1
                        except InterruptedError:
                            raise
                        except (OSError, wave.Error, RuntimeError, TimeoutError) as error:
                            self.warn("第 %d 幕原视频 %s 音轨不可用，改为静音：%s" % (
                                index + 1, Path(segment["source"]).name, str(error)[:150]))
                    raw += part
                    copied += frame_count
                raw = raw[:expected * 2]
                writer.writeframesraw(raw)
                if len(raw) < expected * 2:
                    writer.writeframesraw(bytes(expected * 2 - len(raw)))
            writer.writeframes(b"")
        if not sound_count or wav_rms(destination) < .0001:
            destination.unlink(missing_ok=True)
            return None
        self.log("已保留 %d 段用户视频的原声，并自动对齐镜头时间线" % sound_count)
        return destination

    def background_audio_playlist(self, sources):
        if not sources:
            raise ValueError("未提供背景音乐")
        if len(sources) == 1:
            return sources[0]
        destination = self.job / "user_background_playlist.wav"
        args = [self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
        parts = []
        for index, path in enumerate(sources):
            if not Path(path).is_file():
                raise RuntimeError("背景音乐文件丢失：" + Path(path).name)
            args.extend(["-i", str(path)])
            parts.append("[%d:a]aresample=%d,aformat=sample_fmts=s16:channel_layouts=mono,"
                         "asetpts=PTS-STARTPTS[s%d]" % (index, SPEECH_RATE, index))
        filtergraph = ";".join(parts + ["".join("[s%d]" % index for index in range(len(sources))) +
                                        "concat=n=%d:v=0:a=1[music]" % len(sources)])
        args.extend(["-filter_complex", filtergraph, "-map", "[music]", "-c:a", "pcm_s16le", str(destination)])
        run_external(args, self.root, log=self.log, cancel=self.cancel,
                     timeout=max(180, int(len(sources) * FFMPEG_INPUT_TIMEOUT)), capture=True)
        if not destination.is_file() or destination.stat().st_size < 2000:
            raise RuntimeError("无法合并用户指定的多段背景音乐")
        self.log("已依照导入顺序合并 %d 段音频，不会只采用第一段" % len(sources))
        return destination


    def combine_audio(self, mute_video, voice, seconds, mood, seed, result,
                      voice_gain=1.1, background_gain=.17, ambient_gain=None):
        if wav_rms(voice) < .0007:
            raise RuntimeError("合成旁白接近静音，禁止交付无声视频")
        mus = self.job / "music.wav"
        supplied = self.request["files"].get("音频", [])
        if supplied and self.request.get("audio_role") == "作为背景音乐":
            source = self.background_audio_playlist(supplied)
            self.log("使用用户提供的背景音乐：" + str(source))
        else:
            generate_music(mus, seconds, mood, seed)
            source = mus
        args = [self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(mute_video),
                "-i", str(voice), "-stream_loop", "-1", "-i", str(source)]
        ambient = getattr(self, "ambient_audio", None)
        if ambient and Path(ambient).is_file():
            args.extend(["-i", str(ambient)])
            priority = self.request.get("source_audio_role") == "原声优先"
            mix = ("[1:a]volume=%.3f,asplit=3[voice][key][voicekey];"
                   "[2:a]volume=%.3f[bg];"
                   "[bg][key]sidechaincompress=threshold=0.025:ratio=6:attack=30:release=280[duck];"
                   "[3:a]volume=%.3f[amb];"
                   "[amb][voicekey]sidechaincompress=threshold=0.028:ratio=5:attack=25:release=280[ambduck];"
                   "[voice][duck][ambduck]amix=inputs=3:duration=first:dropout_transition=0:normalize=0,"
                   "alimiter=limit=0.95[mix]") % (voice_gain, min(background_gain, .10) if priority
                                                   else background_gain,
                                                   .65 if priority and ambient_gain is None else
                                                   AMBIENT_VOLUME if ambient_gain is None else ambient_gain)
        else:
            mix = ("[1:a]volume=%.3f,asplit=2[voice][key];"
                   "[2:a]volume=%.3f[bg];"
                   "[bg][key]sidechaincompress=threshold=0.025:ratio=6:attack=30:release=280[duck];"
                   "[voice][duck]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
                   "alimiter=limit=0.95[mix]") % (voice_gain, background_gain)
        args.extend(["-filter_complex", mix, "-map", "0:v:0", "-map", "[mix]", "-c:v", "copy",
                     "-c:a", "aac", "-b:a", "160k", "-t", "%.3f" % seconds,
                     "-movflags", "+faststart", str(result)])
        run_external(args, self.root, log=self.log, cancel=self.cancel, timeout=300, capture=True)
        return result

    def inspect_temporal_bursts(self, source, durations):
        cursor = 0.0
        reviews = []
        for index, length in enumerate(durations):
            self.models.check_stop()
            if length < .6:
                reviews.append({"scene": index, "status": REVIEW_NOT_APPLICABLE,
                                "reason": "镜头短于可靠连续帧检查窗口"})
                cursor += length
                continue
            visual_segments = read_json(self.job / ("scene_%02d.json" % index), {}).get("image", {}).get("montage", [])
            cuts = []
            if isinstance(visual_segments, list) and len(visual_segments) > 1:
                elapsed = 0.0
                for part in visual_segments[:-1]:
                    elapsed += max(0.0, float(part.get("seconds", 0)))
                    cuts.append(elapsed)
            for slot, fraction in enumerate((.12, .50, .88)):
                local = max(0.0, min(length - (MIN_MOTION_REVIEW_FRAMES + 2) / self.fps, length * fraction))
                if any(abs(local - cut) < 4 / self.fps for cut in cuts):
                    continue
                midpoint = cursor + local
                base = self.job / ("temporal_%02d_%d" % (index, slot))
                files = [Path(str(base) + "_%02d.png" % number) for number in range(1, 4)]
                failure = None
                for attempt in range(MAX_TEMPORAL_RETRIES + 1):
                    self.models.check_stop()
                    for item in files:
                        item.unlink(missing_ok=True)
                    try:
                        run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                                      "-ss", "%.5f" % midpoint, "-i", str(source),
                                      "-vf", "scale=128:72", "-frames:v", str(MIN_MOTION_REVIEW_FRAMES),
                                      str(base) + "_%02d.png"], self.root, cancel=self.cancel,
                                     timeout=85, capture=True)
                        if not all(item.is_file() for item in files):
                            raise RuntimeError("未提取到完整的连续三帧")
                        differences = [round(image_mean_difference(a, b), 3)
                                       for a, b in zip(files, files[1:])]
                        suspicious = all(item >= MAX_NEIGHBOR_FRAME_DIFFERENCE for item in differences)
                        reviews.append({"scene": index, "position": round(midpoint, 3),
                                        "neighbor_differences": differences,
                                        "suspected_flicker": suspicious,
                                        "status": REVIEW_FAIL if suspicious else REVIEW_PASS,
                                        "attempts": attempt + 1})
                        failure = None
                        break
                    except InterruptedError:
                        raise
                    except (OSError, RuntimeError, ValueError, TimeoutError) as error:
                        failure = error
                        if attempt < MAX_TEMPORAL_RETRIES:
                            self.resources.adaptive_pause("temporal_retry", self.cancel)
                if failure is not None:
                    reviews.append({"scene": index, "position": round(midpoint, 3),
                                    "status": REVIEW_UNAVAILABLE, "attempts": MAX_TEMPORAL_RETRIES + 1,
                                    "error_type": type(failure).__name__, "error": str(failure)[:170]})
            cursor += length
        return reviews

    def review_spoken_narration(self, final_video, durations):
        report = []
        cursor = 0.0
        for index, duration in enumerate(durations):
            self.models.check_stop()
            record = read_json(self.job / ("scene_%02d.json" % index), {})
            original = record.get("voice")
            scene = self.active_plan["scenes"][index]
            if not original or not Path(original).is_file():
                report.append({"scene": index, "status": "missing_voice"})
                cursor += duration
                continue
            extracted = self.job / ("mix_review_%02d.wav" % index)
            try:
                run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                              "-i", str(final_video), "-ss", "%.6f" % cursor,
                              "-t", "%.6f" % duration, "-map", "0:a:0", "-vn",
                              "-ac", "1", "-ar", str(SPEECH_RATE),
                              "-c:a", "pcm_s16le", str(extracted)],
                             self.root, log=self.log, cancel=self.cancel,
                             timeout=max(FFMPEG_INPUT_TIMEOUT, int(duration * 20)), capture=True)
                mixed_rms = wav_rms(extracted)
                original_rms = wav_rms(original)
                correlation = voice_presence_correlation(original, extracted)
                base = {"scene": index, "start": round(cursor, 4),
                        "source_rms": round(original_rms, 6),
                        "mixed_rms": round(mixed_rms, 6),
                        "voice_correlation": round(correlation, 4),
                        "actual_track": str(final_video)}
                if (mixed_rms < MIN_MIXED_VOICE_RMS or
                        correlation < MIN_MIXED_VOICE_CORRELATION):
                    report.append({**base, "status": "mix_voice_missing"})
                    cursor += duration
                    continue
                original_text = self.models.transcribe(original, self.job, self.log,
                                                      max_seconds=min(duration + .5, ASR_WINDOW_SECONDS * 2),
                                                      include_timestamps=False, language="zh")
                mixed_text = self.models.transcribe(extracted, self.job, self.log,
                                                   max_seconds=min(duration + .5, ASR_WINDOW_SECONDS * 2),
                                                   include_timestamps=False, language="zh")
                source_match = speech_match(scene["narration"], original_text)
                mixed_match = speech_match(scene["narration"], mixed_text)
                report.append({**base, "status": "reviewed", "source": source_match,
                               "mixed": mixed_match,
                               "method": "final_mp4_aac_track_and_source_asr_with_waveform_correlation"})
            except InterruptedError:
                raise
            except (RuntimeError, OSError, ValueError, MemoryError, TimeoutError, wave.Error) as error:
                report.append({"scene": index, "status": "recognition_unavailable",
                               "failure": str(error)[:240], "actual_track": str(final_video)})
            cursor += duration
        atomic_json(self.job / "speech_review.json", report)
        return report

    def check_final(self, path, seconds, scene_durations=None):
        result = {"passed": False, "file": str(path), "expected_seconds": round(seconds, 3),
                  "checked": datetime.datetime.now().isoformat()}
        if not Path(path).is_file() or Path(path).stat().st_size < 8192:
            result["failure_code"] = "OUTPUT_MISSING"
            result["failure"] = "成片不存在或大小异常"
            return result
        self.log("检查成片全部音视频流、时长及抽样画面")
        try:
            output = run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-xerror",
                                   "-i", str(path), "-map", "0:v:0", "-map", "0:a:0",
                                   "-progress", "pipe:1", "-f", "null", "-"],
                                  self.root, cancel=self.cancel, timeout=max(240, int(seconds * 18)), capture=True)
        except (RuntimeError, TimeoutError, OSError) as error:
            result["failure_code"] = "DECODE_FAILURE"
            result["failure"] = "音视频流缺失或解码失败：" + str(error)[:500]
            return result
        progress = re.findall(r"out_time_(?:us|ms)=(\d+)", output)
        if not progress:
            result["failure_code"] = "DURATION_UNREADABLE"
            result["failure"] = "无法读取完整解码后的媒体时长"
            return result
        actual_seconds = int(progress[-1]) / 1000000
        result["actual_seconds"] = round(actual_seconds, 3)
        allowed = max(.18, seconds * MAX_FINAL_DURATION_DRIFT)
        if abs(actual_seconds - seconds) > allowed:
            result["failure_code"] = "DURATION_MISMATCH"
            result["failure"] = "视频长度与分镜时长偏差过大"
            return result
        probes = {}
        probe_masks = {}
        captions = read_json(self.job / "subtitle_timeline.json", [])
        if scene_durations:
            cursor = 0.0
            for scene_index, duration in enumerate(scene_durations):
                caption_record = (captions[scene_index] if isinstance(captions, list) and
                                  scene_index < len(captions) and isinstance(captions[scene_index], dict)
                                  else {})
                if duration > .5 and not caption_record.get("segments"):
                    position = round(cursor + duration * .5, 3)
                    probes[position] = scene_index
                if isinstance(captions, list) and scene_index < len(captions) and isinstance(captions[scene_index], dict):
                    for segment in captions[scene_index].get("segments", []):
                        if isinstance(segment, dict):
                            start = float(segment.get("start", 0))
                            end = float(segment.get("end", 0))
                            if 0 <= start < end <= duration + 1 / self.fps:
                                point = round(cursor + (start + end) / 2, 3)
                                probes[point] = scene_index
                                probe_masks[point] = segment.get("path")
                cursor += duration
        else:
            probes = {round(max(.5, min(seconds - .4, seconds * ratio)), 3): None
                      for ratio in (.2, .5, .8)}
        endpoints = {}
        if self.request["files"].get("首帧"):
            endpoints[0.0] = 0
        if self.request["files"].get("尾帧"):
            endpoints[round(max(0.0, min(actual_seconds, seconds) - 2 / self.fps), 3)] = (
                len(scene_durations) - 1 if scene_durations else None)
        probes.update(endpoints)
        positions = sorted(probes)
        semantic_reviews = []
        semantic_unreviewed = []
        for index, position in enumerate(positions):
            frame_path = self.job / ("final_check_%02d.png" % index)
            try:
                run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
                              "-ss", str(position), "-i", str(path), "-frames:v", "1", str(frame_path)],
                             self.root, cancel=self.cancel, timeout=80, capture=True)
                valid, reason = validate_image(frame_path, allow_flat=position in endpoints)
                if valid and position in endpoints and probes[position] is not None:
                    from PIL import Image, ImageChops, ImageStat
                    expected_source = (self.request["files"]["首帧"][0] if position == 0.0 else
                                       self.request["files"]["尾帧"][0])
                    expected_image = self.job / ("boundary_expected_%02d.png" % probes[position])
                    frame_with_caption(expected_source, expected_image, self.size, "", "")
                    if expected_image.is_file():
                        with Image.open(expected_image) as reference, Image.open(frame_path) as rendered:
                            baseline = reference.convert("RGB").resize((128, 128))
                            observed = rendered.convert("RGB").resize((128, 128))
                            delta = sum(ImageStat.Stat(ImageChops.difference(baseline, observed)).mean) / 3
                        if delta > BOUNDARY_FRAME_MEAN_DIFF_MAX:
                            valid, reason = False, "首尾画面与用户指定素材不一致（偏差 %.1f）" % delta
            except (RuntimeError, OSError, TimeoutError, ValueError) as error:
                valid, reason = False, str(error)
            if not valid:
                result["failure_code"] = "SCENE_FRAME_INVALID"
                result["failure"] = "成片在 %.2f 秒处出现异常画面：%s" % (position, reason)
                if probes[position] is not None:
                    result["scene"] = probes[position]
                elif scene_durations:
                    cursor = 0
                    for scene_index, duration in enumerate(scene_durations):
                        cursor += duration
                        if position <= cursor:
                            result["scene"] = scene_index
                            break
                return result
            scene_index = probes[position]
            if scene_index is not None and position not in endpoints:
                saved_visual = read_json(self.job / ("scene_%02d.json" % scene_index), {}).get("image", {})
                local_position = position - sum(scene_durations[:scene_index]) if scene_durations else 0
                segments = saved_visual.get("overlays", [])
                active_segment = next((entry for entry in segments if
                                       entry.get("start", -1) <= local_position <
                                       entry.get("end", -1) - CAPTION_SEGMENT_GAP_FRAMES / self.fps), None)
                mask = probe_masks.get(position) or (active_segment or {}).get("path")
                if mask and Path(mask).is_file():
                    try:
                        readable, detail = caption_visible(mask, frame_path)
                    except (OSError, ValueError) as error:
                        readable, detail = False, {"error": str(error)[:180]}
                    if not readable:
                        result.update({"failure_code": "CAPTION_VISIBILITY", "scene": scene_index,
                                       "caption_visibility": detail,
                                       "failure": "第 %d 幕成片字幕可能被遮挡或未正确叠加" % (scene_index + 1)})
                        return result
                else:
                    result.update({"failure_code": "CAPTION_VISIBILITY", "scene": scene_index,
                                   "failure": "字幕参考遮罩丢失或时段配置有缺漏，无法确认文字是否可见"})
                    return result
            if (scene_index is not None and position not in endpoints
                    and hasattr(self, "active_plan") and scene_index < len(self.active_plan["scenes"])):
                saved = read_json(self.job / ("scene_%02d.json" % scene_index), {})
                baseline = saved.get("image", {}).get("metrics")
                if not isinstance(baseline, dict) or baseline.get("semantic_passed") is None:
                    semantic_unreviewed.append({"scene": scene_index,
                                                "status": "not_checked",
                                                "reason": "扩展离线审校未准备好或未记录"})
                elif baseline.get("semantic_passed") is False:
                    semantic_unreviewed.append({"scene": scene_index,
                                                "status": "user_supplied_conflict",
                                                "reason": "保留用户指定素材，未声称语义通过"})
                elif baseline.get("passed"):
                    try:
                        semantics = self.models.image_similarity(
                            frame_path, self.active_plan["scenes"][scene_index]["visual_prompt"])
                    except InterruptedError:
                        raise
                    except (RuntimeError, OSError, ValueError, MemoryError) as error:
                        result.update({"failure_code": "SEMANTIC_REVIEW_UNAVAILABLE", "scene": scene_index,
                                       "failure": "成片 AI 语义复检无法完成：" + str(error)[:280]})
                        return result
                    original = float(baseline.get("cosine", MIN_CLIP_COSINE))
                    retention = max(MIN_CLIP_ABSOLUTE_COSINE, original * MIN_FINAL_SEMANTIC_RETENTION)
                    minimum_margin = max(MIN_CLIP_ABSOLUTE_MARGIN,
                                         float(baseline.get("margin", MIN_CLIP_MARGIN)) * .30)
                    accepted = (semantics["cosine"] >= retention and
                                semantics["margin"] >= minimum_margin and
                                semantics["subject_margin"] >= MIN_CLIP_ABSOLUTE_MARGIN)
                    semantic_reviews.append({"scene": scene_index, "position": position,
                                             "original_cosine": original,
                                             "final": semantics, "required_cosine": round(retention, 4),
                                             "required_margin": round(minimum_margin, 4), "passed": accepted})
                    if not accepted:
                        result.update({"failure_code": "FINAL_SEMANTIC_MISMATCH", "scene": scene_index,
                                       "semantic_reviews": semantic_reviews,
                                       "failure": "第 %d 幕成片画面偏离已审校的生成内容" % (scene_index + 1)})
                        return result
        temporal_reviews = self.inspect_temporal_bursts(path, scene_durations or [seconds])
        result["temporal_reviews"] = temporal_reviews
        temporal_unreviewed = []
        for review in temporal_reviews:
            index = review["scene"]
            checkpoint = read_json(self.job / ("scene_%02d.json" % index), {})
            visual = checkpoint.get("image", {})
            user_supplied = bool(visual.get("metrics", {}).get("user_supplied"))
            if review.get("status") == REVIEW_UNAVAILABLE:
                if not user_supplied:
                    result.update({"failure_code": "TEMPORAL_REVIEW_UNAVAILABLE", "scene": index,
                                   "failure": "第 %d 幕连续帧审校重试后仍不可用，不能宣称已通过" % (index + 1),
                                   "temporal_unreviewed": [review]})
                    return result
                temporal_unreviewed.append(review)
                self.warn("第 %d 幕用户素材的连续帧审核未完成，保留素材并标记未审校" % (index + 1))
            elif review.get("status") == REVIEW_NOT_APPLICABLE:
                temporal_unreviewed.append(review)
            elif review.get("status") == REVIEW_FAIL:
                if visual.get("type") in {"image", "native_video"} and not user_supplied:
                    result.update({"failure_code": "TEMPORAL_FLICKER", "scene": index,
                                   "failure": "检测到相邻帧可能发生严重闪烁，需修复第 %d 幕" % (index + 1)})
                    return result
                temporal_unreviewed.append(review)
                self.warn("第 %d 幕用户原始视频包含强烈快速变化，已保留用户素材" % (index + 1))
        result["temporal_unreviewed"] = temporal_unreviewed
        preview = self.job / "final_preview.png"
        shutil.copy2(self.job / ("final_check_%02d.png" % (len(positions) // 2)), preview)
        try:
            audio_scan = run_external([self.ffmpeg, "-hide_banner", "-nostdin", "-i", str(path),
                                       "-vn", "-af", "volumedetect", "-f", "null", "-"],
                                      self.root, cancel=self.cancel, timeout=max(120, int(seconds * 5)), capture=True)
            found = re.search(r"mean_volume:\s*(-?inf|-?[\d.]+)\s*dB", audio_scan)
            if not found or found.group(1) == "-inf" or float(found.group(1)) < -65:
                result["failure_code"] = "AUDIO_LOW"
                result["failure"] = "成片声轨检测为静音或过低，拒绝交付"
                return result
            result["mean_volume_db"] = float(found.group(1))
        except (RuntimeError, TimeoutError, OSError, ValueError) as error:
            result["failure_code"] = "AUDIO_SCAN_FAILED"
            result["failure"] = "成片声音检查失败：" + str(error)[:350]
            return result
        if scene_durations:
            if not isinstance(captions, list) or len(captions) != len(scene_durations):
                result.update({"failure_code": "CAPTION_TIMELINE_MISSING",
                               "failure": "字幕时间线记录缺失或镜头数量不匹配"})
                return result
            cursor = 0.0
            caption_checks = []
            for index, (caption, duration) in enumerate(zip(captions, scene_durations)):
                scene = self.active_plan["scenes"][index]
                valid = isinstance(caption, dict) and isinstance(caption.get("segments"), list)
                parts = caption.get("segments", []) if valid else []
                if valid:
                    valid = bool(parts) and all(isinstance(part, dict) for part in parts)
                if valid:
                    try:
                        reconstructed = normalized_caption("".join(str(part.get("text", "")) for part in parts))
                        voice = caption.get("voice_file")
                        voice_seconds = float(caption.get("voice_seconds", -1))
                        valid = (caption.get("caption") == scene.get("narration") and
                                 abs(float(caption.get("from", -1)) - cursor) <= 2 / self.fps and
                                 abs(float(caption.get("to", -1)) - cursor - duration) <= 2 / self.fps and
                                 0 < voice_seconds <= duration + .05 and math.isfinite(voice_seconds) and
                                 isinstance(voice, str) and Path(voice).is_file() and
                                 file_integrity_hash(voice) == caption.get("voice_sha256") and
                                 reconstructed == normalized_caption(scene.get("narration", "")))
                        prior_end = 0.0
                        for part in parts:
                            filename = part.get("path")
                            start = float(part.get("start", -1))
                            end = float(part.get("end", -1))
                            if (not isinstance(filename, str) or not Path(filename).is_file() or
                                    not all(math.isfinite(value) for value in (start, end)) or
                                    not 0 <= start < end <= duration + 1 / self.fps or
                                    start + 1 / self.fps < prior_end or
                                    full_file_sha256(filename) != part.get("sha256")):
                                valid = False
                                break
                            prior_end = end
                    except (OSError, TypeError, ValueError, OverflowError):
                        valid = False
                if not valid:
                    result.update({"failure_code": "CAPTION_TIMELINE_MISMATCH", "scene": index,
                                   "failure": "字幕分页文字、可见时段、校验和或对应旁白与分镜不一致"})
                    return result
                caption_checks.append({"scene": index, "pages": len(parts), "voice_verified": True,
                                       "full_text_covered": True})
                cursor += duration
            result["caption_manifest_verified"] = True
            result["caption_checks"] = caption_checks
        result["frames_checked"] = positions
        result["semantic_reviews"] = semantic_reviews
        result["semantic_unreviewed"] = semantic_unreviewed
        if scene_durations and self.capabilities["speech_review"]:
            speech_reviews = self.review_spoken_narration(path, scene_durations)
            result["speech_reviews"] = speech_reviews
            for review in speech_reviews:
                issue = speech_review_failure(review)
                if issue:
                    result.update({"failure_code": issue, "scene": review["scene"],
                                   "failure": "第 %d 幕成片真实音轨与原旁白不符或声音不可辨认：%s" %
                                   (review["scene"] + 1, issue)})
                    return result
        else:
            result["speech_reviews"] = [{"status": "not_checked", "reason": "语音识别模型未验收"}]
        if not scene_durations:
            result["review_level"] = "technical_only"
        elif semantic_unreviewed or temporal_unreviewed:
            result["review_level"] = "partially_reviewed"
        elif not self.capabilities.get("semantic_review") or not self.capabilities.get("speech_review"):
            result["review_level"] = "partially_reviewed"
        elif any(review.get("status") != "reviewed" or any(
                review.get(role, {}).get("status") not in {"matched", "empty_expected"}
                for role in ("source", "mixed")) for review in result.get("speech_reviews", [])):
            result["review_level"] = "partially_reviewed"
        else:
            result["review_level"] = "multimodal_heuristic_reviewed"
        result["checks"] = {"decode": True, "duration": True, "sampled_frames": True,
                            "temporal_neighbors": sum(review.get("status") == REVIEW_PASS
                                                      for review in temporal_reviews),
                            "temporal_unreviewed": len(temporal_unreviewed),
                            "audio_presence": True,
                            "subtitle_timeline": bool(scene_durations), "caption_visibility": True,
                            "content_semantics": "CLIP 启发式复检及显式文字约束审查；身份、数量、真实动作和事实无法被此模型可靠证明",
                            "subtitle_text": "字幕原文、时间轴及遮罩文件已检查；未声称 OCR 逐字验证",
                            "speech_synchronization": "成片实际 AAC 音轨逐幕提取，配合源音轨 ASR 与波形相关性复检"}
        result["limitations"] = ["CLIP 不能严格验证精确数量、人物身份、历史事实和动作完成度",
                                 "已执行生成提示词约束保留检查及成片多关键帧抽查"]
        result["passed"] = True
        return result

    def start(self):
        set_low_priority()
        try:
            self.models = LocalModels(self.root, lambda s: self.step(s), self.cancel,
                                      quality=self.request.get("quality", "智能"), resources=self.resources)
            self.data["selected_models"] = dict(self.models.model_choices)
            self.resources.start_monitor(self.cancel, self.log)
            self.data["render_mode_requested"] = self.request.get("visual_mode", "智能轻量运镜")
            seconds = int(self.request["duration"])
            pixels = self.size[0] * self.size[1]
            estimated_media = int(seconds * self.fps * pixels * .16) + 240 * 1024 * 1024
            self.resources.ensure("job_preflight", disk_required=MIN_JOB_FREE + estimated_media)
            self.data["disk_budget"] = {"estimated_intermediate_bytes": estimated_media,
                                         "reserve_bytes": MIN_JOB_FREE}
            self.publish_event("phase", phase="preparing")
            self.step("将素材安全保存至工作目录，避免移动设备断开后丢失", 2)
            localized = localize_request_assets(self.root, self.request, self.job, self.cancel,
                                                self.log, self.data)
            self.data["localized_sources"] = localized
            self.data["request"] = self.request
            atomic_json(self.job / "job.json", self.data)
            self.step("检查并恢复链接与缓存素材", 3)
            cpu_mode = self.models.device == "cpu"
            optimal_length = 5.0 if self.capabilities.get("native_video") else (9 if cpu_mode else 6)
            limit_scenes = MAX_NATIVE_SEGMENTS if self.capabilities.get("native_video") else 6
            recommended = max(2, min(limit_scenes, math.ceil(seconds / optimal_length)))
            if any(self.request["files"].get(kind) for kind in ("首帧", "尾帧", "图片", "视频")):
                recommended = max(3, recommended)
            previous_plan = read_json(self.job / "storyboard.json", {})
            saved_scenes = previous_plan.get("scenes") if isinstance(previous_plan, dict) else None
            scenes = (len(saved_scenes) if isinstance(saved_scenes, list) and
                      2 <= len(saved_scenes) <= MAX_NATIVE_SEGMENTS and validate_plan(previous_plan, len(saved_scenes))
                      else recommended)
            timeline = semantic_timeline(seconds, previous_plan["scenes"] if validate_plan(previous_plan, scenes)
                                         else [{"narration": ""} for _ in range(scenes)], self.fps)
            self.publish_event("phase", phase="planning")
            if validate_plan(previous_plan, scenes):
                self.step("恢复已有分镜，继续未完成的镜头", 14)
                plan = previous_plan
            else:
                self.step("理解提示词及全部素材", 4)
                reference = self.gather_inputs()
                self.models.listener = None
                self.models.listener_processor = None
                gc.collect()
                self.step("AI 编写文案、分镜与配乐风格", 12)
                plan = self.models.plan(self.request["prompt"], reference, scenes, seconds)
                atomic_json(self.job / "storyboard.json", plan)
            timeline = semantic_timeline(seconds, plan["scenes"], self.fps)
            for index, scene in enumerate(plan["scenes"]):
                scene["seconds"] = timeline[index]
                if narration_units(scene["narration"]) > timeline[index] * 3.2:
                    scene["narration"] = self.rewrite_narration(scene["narration"], timeline[index])
            atomic_json(self.job / "storyboard.json", plan)
            self.models.unload_director()
            self.publish_event("storyboard", title=plan["title"], scenes=[
                {"narration": scene["narration"], "seconds": scene["seconds"]}
                for scene in plan["scenes"]])
            self.publish_event("phase", phase="rendering")
            self.step("分镜结构已检查，开始生成素材", 20)
            clips, voice, real_seconds, assets = self.compose_clips(plan)
            lengths = [read_json(self.job / ("scene_%02d.json" % i), {}).get("duration", seconds / scenes)
                       for i in range(len(plan["scenes"]))]
            self.ambient_audio = self.build_original_audio(lengths)
            self.publish_event("phase", phase="finishing")
            self.step("剪辑：统一帧率、镜头尺寸与过渡", 83)
            joined = self.job / "edited_no_audio.mp4"
            self.concat_clips(clips, joined)
            self.step("混音并完整检查成片", 90)
            output = self.result_dir / "final.mp4"
            temp_output = self.job / "final_first_pass.mp4"
            seed = int(hashlib.sha256(self.request["prompt"].encode("utf-8")).hexdigest()[:8], 16)
            self.combine_audio(joined, voice, real_seconds, plan.get("mood", "inspiring"), seed, temp_output)
            verdict = self.check_final(temp_output, real_seconds, lengths)
            reviews = [verdict]
            for attempt in range(MAX_REPAIR_PASSES):
                if verdict["passed"]:
                    break
                self.step("成片检查未通过，按失败原因修复并复检", 94 + attempt * 2)
                self.log("成片检查失败：" + verdict.get("failure", "未知原因"))
                modified = self.job / ("final_repair_%d.mp4" % attempt)
                failure_code = verdict.get("failure_code", "UNKNOWN")
                action = repair_action_for(failure_code)
                repair_record = {"at": now_stamp(), "failure_code": failure_code,
                                 "cause": verdict.get("failure", ""), "action": action,
                                 "round": attempt + 1,
                                 "before_metrics": {key: value for key, value in verdict.items()
                                                    if key not in {"semantic_reviews", "temporal_reviews"}}}
                self.data.setdefault("repairs", []).append(repair_record)
                if action == "restart_reviewer_and_recheck":
                    self.log("审核组件暂不可用：只恢复审核器并复检，保留已生成的画面和声音")
                    if failure_code == "SEMANTIC_REVIEW_UNAVAILABLE":
                        self.models.unload_inspector()
                        self.models.inspector_failed = False
                    elif failure_code == "SPEECH_REVIEW_UNAVAILABLE":
                        self.models.listener = None
                        self.models.listener_processor = None
                    else:
                        self.log("重新提取连续视频帧并复核，不重新生成已合格的画面")
                    gc.collect()
                    self.resources.adaptive_pause("review_recovery", notify=self.log)
                    modified = temp_output
                elif failure_code == "CAPTION_TIMELINE_MISSING":
                    self.log("仅重建全部字幕与语音的校验记录，不重新生成画面")
                    voices = [read_json(self.job / ("scene_%02d.json" % i), {})["voice"]
                              for i in range(len(plan["scenes"]))]
                    self.write_subtitle_timeline(plan["scenes"], lengths, voices)
                    modified = temp_output
                elif failure_code in {"MIXED_VOICE_MISSING", "MIXED_SPEECH_MISMATCH",
                                      "MIXED_AUDIO_EXTRACTION_FAILED"}:
                    self.log("成片实际音轨未通过复检，增强旁白并降低背景与素材原声后重新混音")
                    self.combine_audio(joined, voice, real_seconds, plan.get("mood", "inspiring"), seed,
                                       modified, voice_gain=1.4 + attempt * .12,
                                       background_gain=.06 if attempt == 0 else .015,
                                       ambient_gain=.05 if attempt == 0 else 0)
                elif "scene" in verdict:
                    preserve = ({verdict["scene"]} if action in {
                        "reencode_caption_keep_visual", "disable_synthetic_motion_keep_visual"} else set())
                    if action == "disable_synthetic_motion_keep_visual":
                        self.motion_safe_scenes.add(verdict["scene"])
                    action = "重新排版/编码字幕，复用合格画面" if preserve else "重新生成或编码有缺陷的画面"
                    self.log("定向修复第 %d 幕：%s" % (verdict["scene"] + 1, action))
                    clips, voice, real_seconds, assets = self.compose_clips(
                        plan, force_scenes={verdict["scene"]}, repair_round=attempt + 1,
                        preserve_visual=preserve)
                    lengths = [read_json(self.job / ("scene_%02d.json" % i), {}).get("duration", seconds / scenes)
                               for i in range(len(plan["scenes"]))]
                    self.ambient_audio = self.build_original_audio(lengths)
                    self.concat_clips(clips, joined)
                    self.combine_audio(joined, voice, real_seconds, plan.get("mood", "inspiring"), seed, modified)
                elif failure_code in {"AUDIO_LOW", "AUDIO_SCAN_FAILED", "OUTPUT_MISSING"}:
                    self.log("音频或封装异常，优先重新混音，不重复生成镜头")
                    self.combine_audio(joined, voice, real_seconds, plan.get("mood", "inspiring"), seed,
                                       modified, voice_gain=1.35 + attempt * .15, background_gain=.10)
                else:
                    normalized = self.job / ("edited_repair_%d.mp4" % attempt)
                    filters = "fps=%d,setpts=N/(%d*TB)" % (self.fps, self.fps)
                    run_external([self.ffmpeg, "-hide_banner", "-loglevel", "error", "-y", "-i", str(joined),
                                  "-vf", filters, "-frames:v", str(round(real_seconds * self.fps)),
                                  "-c:v", "libx264", "-preset", "veryfast", "-crf", "25",
                                  "-pix_fmt", "yuv420p", "-an", str(normalized)],
                                 self.root, log=self.log, cancel=self.cancel, timeout=480, capture=True)
                    self.combine_audio(normalized, voice, real_seconds, plan.get("mood", "inspiring"), seed, modified)
                verdict = self.check_final(modified, real_seconds, lengths)
                repair_record["after_metrics"] = {key: value for key, value in verdict.items()
                                                   if key not in {"semantic_reviews", "temporal_reviews"}}
                repair_record["verified"] = bool(verdict.get("passed"))
                atomic_json(self.job / "job.json", self.data)
                reviews.append(verdict)
                if verdict["passed"]:
                    temp_output = modified
            atomic_json(self.job / "final_reviews.json", reviews)
            if not verdict["passed"]:
                raise RuntimeError("成片复检仍未通过：%s。可点击黑匣子导出诊断" % verdict.get("failure", "未知原因"))
            tmp_output = output.with_name(output.name + "." + secrets.token_hex(5) + ".partial.mp4")
            try:
                shutil.copy2(temp_output, tmp_output)
                os.replace(tmp_output, output)
            finally:
                tmp_output.unlink(missing_ok=True)
            shutil.copy2(self.job / "storyboard.json", self.result_dir / "storyboard.json")
            subtitles = self.job / "subtitle_timeline.json"
            if subtitles.is_file():
                shutil.copy2(subtitles, self.result_dir / "subtitle_timeline.json")
            screenshot = self.job / "final_preview.png"
            if screenshot.exists():
                shutil.copy2(screenshot, self.result_dir / "cover.png")
            self.data.update({"status": "完成", "finished": datetime.datetime.now().isoformat(),
                              "render_modes": [item.get("type", "unknown") for item in assets],
                              "render_methods": [item.get("render_method", "unknown") for item in assets],
                              "render_method_note": "真实动态视频只指 CogVideoX 生成镜头；图片动态运镜仅为平移缩放剪辑",
                              "resource_report": self.resources.report(),
                              "output": str(output), "duration": round(real_seconds, 2),
                              "resolution": list(self.size), "scene_count": len(plan["scenes"]),
                              "assets": assets, "final_review": verdict,
                              "semantic_review_coverage": {"reviewed_samples": len(verdict.get("semantic_reviews", [])),
                                                           "unreviewed_samples": len(verdict.get("semantic_unreviewed", []))}})
            atomic_json(self.job / "job.json", self.data)
            atomic_json(self.result_dir / "manifest.json", self.data)
            self.publish_event("phase", phase="complete")
            completion = ("成片已保存，技术检查通过；部分素材未完成 AI 语义审校，请查看交付报告"
                          if verdict.get("review_level") != "multimodal_heuristic_reviewed" else
                          "成片已保存，多模态启发式复检通过；请查看交付报告")
            self.step(completion, 100)
            return output
        except Exception as error:
            self.data["status"] = "已停止" if isinstance(error, InterruptedError) else "失败"
            self.data["error"] = traceback.format_exc()
            self.data["error_code"] = ("RESOURCE_EXHAUSTED" if self.resources.resource_stop_reason else
                                       "USER_STOP" if isinstance(error, InterruptedError) else
                                       "RESOURCE_EXHAUSTED" if is_memory_error(error) else
                                       "INPUT_UNAVAILABLE" if isinstance(error, (OSError, FileNotFoundError)) else
                                       "PIPELINE_ERROR")
            self.data["resource_report"] = self.resources.report()
            atomic_json(self.job / "job.json", self.data)
            raise
        finally:
            self.resources.stop_monitor()
            if self.piper_worker is not None:
                self.piper_worker.close()
                self.piper_worker = None
            if self.models:
                self.models.close()


def preferred_desktop():
    if os.name == "nt":
        try:
            buffer = ctypes.create_unicode_buffer(4096)
            if ctypes.windll.shell32.SHGetFolderPathW(None, 0x0010, None, 0, buffer) == 0:
                location = Path(buffer.value)
                if location.exists():
                    return location
        except (OSError, AttributeError):
            pass
    candidates = [Path.home() / "Desktop", Path.home() / "OneDrive" / "Desktop"]
    candidates.extend(Path.home().glob("OneDrive*/Desktop"))
    valid = next((item for item in candidates if item.is_dir()), None)
    if valid is None:
        raise RuntimeError("无法确定系统桌面的实际位置，黑匣子未保存到其他目录；请检查桌面文件夹")
    return valid


def cleanup_completed_cache(root, cancel=None):
    root = Path(root)
    cancel = cancel or threading.Event()
    patterns = ("candidate_*.png", "native_review_*.png", "native_seam_*.png",
                "asset_match_*.png", "temporal_*.png", "final_check_*.png",
                "source_audio_*.wav", "mix_review_*.wav", "audio_*.wav")
    totals = {"jobs": 0, "files": 0, "bytes": 0}
    jobs = root / ".studio" / "jobs"
    if jobs.is_dir():
        for folder in jobs.iterdir():
            if cancel.is_set():
                raise InterruptedError("清理已取消")
            if not folder.is_dir() or folder.is_symlink():
                continue
            metadata = read_json(folder / "job.json", {})
            output = metadata.get("output") if isinstance(metadata, dict) else None
            if metadata.get("status") != "完成" or not output or not Path(output).is_file():
                continue
            totals["jobs"] += 1
            for pattern in patterns:
                for file in folder.glob(pattern):
                    if cancel.is_set():
                        raise InterruptedError("清理已取消")
                    if file.is_file() and not file.is_symlink():
                        try:
                            size = file.stat().st_size
                            file.unlink()
                            totals["files"] += 1
                            totals["bytes"] += size
                        except OSError:
                            continue
    temporary = root / ".studio" / "tmp"
    if temporary.is_dir():
        older_than = time.time() - 72 * 3600
        for file in temporary.iterdir():
            if cancel.is_set():
                raise InterruptedError("清理已取消")
            if (file.is_file() and not file.is_symlink() and
                    file.suffix.lower() in {".partial", ".json", ".txt", ".signal"}
                    and file.stat().st_mtime < older_than):
                try:
                    size = file.stat().st_size
                    file.unlink()
                    totals["files"] += 1
                    totals["bytes"] += size
                except OSError:
                    continue
    return totals


def system_report(root, request=None):
    root = Path(root)
    drive = shutil.disk_usage(root)
    report = {
        "app": APP_NAME, "version": APP_VERSION, "time": datetime.datetime.now().isoformat(),
        "os": platform.platform(), "architecture": platform.machine(), "python": sys.version,
        "python_executable": sys.executable, "locale": locale.getlocale(), "cwd": str(Path.cwd()),
        "workspace": str(root), "disk": {"total": drive.total, "used": drive.used, "free": drive.free},
        "memory": memory_info(), "gpu": gpu_info(), "cpu_count": os.cpu_count(),
        "basic_ready": basic_ready(root), "full_ready": is_ready(root),
        "capabilities": capability_report(root, request),
        "model_provenance": model_provenance(root),
        "installed_packages": {tier: packages_healthy(root, tier)
                               for tier in ("basic", "full")},
        "offline_import": read_json(root / ".studio" / "offline_import.json", {}),
        "native_video": {"local_model_detected": bool(native_video_model(root)),
                         "load_verified": native_load_ready(root),
                         "verification": read_json(root / ".studio" / "native_ready.json", {}),
                         "model_class": native_video_model(root)[1] if native_video_model(root) else None},
        "optional_models": {role: optional_model_verified(model_path(root, folder), role)
                            for role, folder in OPTIONAL_MODEL_FOLDERS.items()},
        "environment": {key: os.environ.get(key) for key in (
            "HF_HOME", "HF_ENDPOINT", "TORCH_HOME", "PIP_INDEX_URL", "PYTHONUTF8", "HF_HUB_OFFLINE")},
        "ready_marker": read_json(root / ".studio" / "ready.json", {}),
        "request": request or {},
        "packages": [], "models": [],
        "voice_model": {"repo": VOICE_REPO, "file": str(voice_model_path(root)),
                        "complete": voice_download_complete(root),
                        "download": read_json(model_path(root, "voice") / "download.json", {})},
    }
    site = runtime_site(root)
    try:
        for dist in importlib.metadata.distributions(path=[str(site)]):
            report["packages"].append({"name": dist.metadata.get("Name"), "version": dist.version})
    except Exception as error:
        report["package_error"] = str(error)
    for name, repo, folder, patterns in MODEL_SPECS:
        path = model_path(root, folder)
        weights = []
        for file in path.rglob("*"):
            try:
                if file.is_file() and file.suffix in {".bin", ".safetensors"}:
                    weights.append((str(file.relative_to(path)), file.stat().st_size))
            except OSError:
                continue
        report["models"].append({"name": name, "repo": repo, "folder": str(path), "weights": weights,
                                  "complete": model_download_complete(root, (name, repo, folder, patterns)),
                                 "download": read_json(path / "download.json", {})})
    return report


def diagnostic_exception_summary(value):
    raw = str(value)
    exceptions = re.findall(r"\b([A-Za-z][A-Za-z0-9_]*(?:Error|Exception))\s*:", raw)
    calls = re.findall(r'^\s*File "[^"]+", line (\d+), in ([A-Za-z_][A-Za-z0-9_]*)', raw, re.M)
    wins = re.findall(r"\bWinError\s+(\d+)\b", raw)
    missing = re.findall(r"No module named ['\"]([A-Za-z_][A-Za-z0-9_.]*)['\"]", raw)
    codes = re.findall(r"\b(?:OUTPUT_MISSING|DECODE_FAILURE|DURATION_MISMATCH|DURATION_UNREADABLE|"
                       r"SCENE_FRAME_INVALID|AUDIO_LOW|AUDIO_SCAN_FAILED|FINAL_SEMANTIC_MISMATCH|"
                       r"SEMANTIC_REVIEW_UNAVAILABLE|CAPTION_TIMELINE_MISSING|CAPTION_TIMELINE_MISMATCH|"
                       r"SPEECH_MISMATCH|SPEECH_SOURCE_MISMATCH|SPEECH_SOURCE_MISSING|"
                       r"MIXED_VOICE_MISSING|MIXED_SPEECH_MISMATCH|SPEECH_REVIEW_UNAVAILABLE|"
                       r"MIXED_AUDIO_EXTRACTION_FAILED|TEMPORAL_FLICKER|TEMPORAL_REVIEW_UNAVAILABLE|RESOURCE_EXHAUSTED|"
                       r"INPUT_UNAVAILABLE|PIPELINE_ERROR|USER_STOP)\b", raw)
    return {"exception_type": exceptions[-1] if exceptions else "UnclassifiedError",
            "call_sites": [{"line": int(line), "function": function} for line, function in calls[-8:]],
            "windows_error": int(wins[-1]) if wins else None,
            "failure_code": codes[-1] if codes else None,
            "missing_module": missing[-1] if missing else None,
            "length": len(raw)}


def redact_diagnostic(value, name=""):
    key = name.lower()
    secret_keys = {"prompt", "narration", "visual_prompt", "url", "text", "path", "file",
                   "source", "workspace", "cwd", "python_executable", "output", "result_dir",
                   "last_job", "clip", "voice", "rendered", "overlay", "tokenizer_path",
                   "error", "failure", "warning", "warnings", "exception", "message", "step"}
    if key in secret_keys:
        if key in {"error", "failure", "exception"} and isinstance(value, str):
            return diagnostic_exception_summary(value)
        if key == "warnings" and isinstance(value, list):
            return {"count": len(value)}
        if key == "step" and isinstance(value, str):
            return {"stage_hash": hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]}
        return "[已隐藏]"
    if isinstance(value, dict):
        if name == "gpu":
            card = str(value.get("name", ""))
            driver = str(value.get("driver", ""))
            return {"name": card if len(card) <= 120 and re.fullmatch(r"[A-Za-z0-9_.+() -]*", card) else "[已隐藏]",
                    "driver": driver if re.fullmatch(r"[0-9.]{0,20}", driver) else "[已隐藏]",
                    "free_mb": value.get("free_mb", 0), "total_mb": value.get("total_mb", 0)}
        if name == "request":
            files = value.get("files", {})
            return {"duration": value.get("duration"), "quality": value.get("quality"),
                    "aspect": value.get("aspect"), "audio_role": value.get("audio_role"),
                    "source_audio_role": value.get("source_audio_role"),
                    "prompt_length": len(str(value.get("prompt", ""))),
                    "files_count": {kind: len(paths) for kind, paths in files.items()
                                    if kind in {"首帧", "尾帧", "图片", "音频", "视频", "文档"}}
                    if isinstance(files, dict) else {},
                    "asset_categories": sorted(k for k, v in files.items() if v and k in {"图片", "首帧", "尾帧", "音频", "视频", "文档"})}
        cleaned = {}
        for index, (field, item) in enumerate(value.items()):
            field = str(field)
            safe_key = field if re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", field) or field in {
                "首帧", "尾帧", "图片", "音频", "视频", "文档"} else "field_%04d" % index
            cleaned[safe_key] = redact_diagnostic(item, field)
        return cleaned
    if isinstance(value, (list, tuple)):
        return [redact_diagnostic(item, name) for item in value]
    if isinstance(value, str):
        if key in {"exception_type", "failure_code", "missing_module", "smoke_error_type", "smoke_error_code"}:
            return value if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,80}", value) else "[已隐藏]"
        if key in {"name", "repo", "folder_name"}:
            if value == APP_NAME or value in {item[0] for item in MODEL_SPECS}:
                return value
            if re.fullmatch(r"[a-zA-Z0-9_.+/-]{1,100}", value):
                return value
        if key in {"status", "voice_backend", "quality", "aspect", "audio_role", "source_audio_role", "type", "category"}:
            permitted = {"运行中", "已停止", "完成", "失败", "sapi", "piper", "快速", "智能", "精细",
                         "横屏 16:9", "竖屏 9:16", "方形 1:1", "仅作参考", "作为背景音乐",
                         "自动混合原声", "原声优先", "静音原声",
                         "status", "image", "video", "passed", "ERROR", "INSTALL", "DOWNLOAD", "REVIEW", "RENDER", "STATUS",
                         "network", "resources", "verification", "runtime", "external_process", "repair"}
            return value if value in permitted else "[已隐藏]"
        if key in {"version", "runtime_version", "revision", "sha256", "source_sha256", "model_signature",
                   "request_digest", "python", "torch", "diffusers", "transformers", "pillow",
                   "completed", "started", "finished", "checked", "at", "time", "mtime"}:
            return value if len(value) <= 120 and re.fullmatch(r"[A-Za-z0-9_.:+\s-]+", value) else "[已隐藏]"
        if key in {"os", "architecture"}:
            return value if len(value) <= 120 and re.fullmatch(r"[A-Za-z0-9_.+() -]+", value) else "[已隐藏]"
        if key == "app" and value == APP_NAME:
            return value
        return "[已隐藏]"
    return value


def diagnostic_log_events(lines):
    events = []
    for item in lines[-1200:]:
        stamp = re.match(r"^\[(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?)\]", item)
        if not stamp:
            continue
        has_error = any(term in item for term in ("失败", "异常", "Error", "Exception", "超时", "不足"))
        category = ("ERROR" if has_error else "INSTALL" if "安装" in item else
                    "DOWNLOAD" if "下载" in item else "REVIEW" if "审校" in item or "检查" in item else
                    "RENDER" if "镜头" in item or "编码" in item else "STATUS")
        if category == "STATUS":
            continue
        record = {"at": stamp.group(1), "category": category}
        match = re.search(r"\b([A-Za-z][A-Za-z0-9_]*(?:Error|Exception))\s*:", item)
        if match:
            record["exception_type"] = match.group(1)[:80]
        match = re.search(r"退出码\s*(\d+)", item)
        if match:
            record["exit_code"] = int(match.group(1))
        events.append(record)
    return events[-250:]


def diagnostic_failure_history(lines, job, process_events):
    history = []
    for item in lines[-5000:]:
        if not any(term in item for term in ("失败", "异常", "Error", "Exception", "超时", "不足", "无法")):
            continue
        stamp = re.match(r"^\[(\d{4}-\d\d-\d\dT[^]]+)\]", item)
        raw = item[stamp.end():] if stamp else item
        details = diagnostic_exception_summary(raw)
        category = "network" if any(term in raw for term in ("HTTP", "网络", "连接", "下载", "镜像")) else (
                   "resources" if any(term in raw for term in ("内存", "显存", "磁盘", "不足")) else (
                   "verification" if any(term in raw for term in ("校验", "验收", "审校", "SHA")) else "runtime"))
        history.append({"at": stamp.group(1) if stamp else None,
                        "category": category,
                        "exception_type": details["exception_type"],
                        "failure_code": details["failure_code"],
                        "windows_error": details["windows_error"],
                        "call_sites": details["call_sites"],
                        "message_fingerprint": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]})
    for event in process_events[-200:]:
        if event.get("returncode") not in (None, 0):
            history.append({"at": event.get("at"), "category": "external_process",
                            "exit_code": event.get("returncode")})
    for attempt in job.get("repairs", [])[-100:]:
        if isinstance(attempt, dict):
            history.append({"at": attempt.get("at"), "category": "repair",
                            "failure_code": attempt.get("failure_code"),
                            "round": attempt.get("round")})
    return history[-500:]


def export_black_box(root, request, last_job, notifier, include_private=False):
    root = Path(root)
    desktop = preferred_desktop()
    name = "AI工坊黑匣子_" + now_stamp() + ".zip"
    destination = desktop / name
    temporary = root / ".studio" / "tmp" / (name + ".partial")
    temporary.parent.mkdir(parents=True, exist_ok=True)
    desktop_partial = destination.with_suffix(".partial")
    inventory = []
    omitted = []
    selected = set()
    parts = []
    started = time.monotonic()
    def add_file(path, target=None):
        path = Path(path)
        if not path.is_file() or path.is_symlink():
            return
        target = target or "evidence/" + path.name
        if target in selected:
            return
        if path.stat().st_size > 32 * 1024 * 1024:
            omitted.append({"target": target if include_private else path.suffix.lower(),
                            "reason": "per_file_limit", "bytes": path.stat().st_size})
            return
        selected.add(target)
        parts.append((path, target))
    app_log = root / ".studio" / "logs" / "studio.log"
    if include_private:
        add_file(app_log, "logs/studio.log")
    script = Path(__file__).resolve()
    if include_private:
        add_file(script, "source/" + script.name)
    jobpath = Path(last_job) if last_job else None
    if jobpath is None or not jobpath.is_dir():
        jobs = root / ".studio" / "jobs"
        if jobs.is_dir():
            candidates = sorted(jobs.glob("*/job.json"), key=lambda item: item.stat().st_mtime, reverse=True)
            jobpath = candidates[0].parent if candidates else None
    if jobpath and jobpath.exists():
        for file in jobpath.rglob("*"):
            if time.monotonic() - started > 12:
                break
            allowed = ({".json", ".txt", ".log", ".ps1", ".png", ".jpg", ".wav", ".mp4"}
                       if include_private else {".json"})
            recognized_json = (file.parent == jobpath and file.suffix.lower() == ".json" and
                               file.stat().st_size <= 32 * 1024 * 1024)
            if (file.is_file() and file.suffix.lower() in allowed
                    and (include_private or recognized_json)):
                add_file(file, "last_job/" + file.relative_to(jobpath).as_posix())
    result_folder = root / "成品"
    if result_folder.exists():
        recent = sorted((item for item in result_folder.iterdir() if item.is_dir()), reverse=True)[:2]
        for folder_number, folder in enumerate(recent, 1):
            for file in folder.iterdir():
                if (file.suffix.lower() in ({".json", ".png", ".mp4"} if include_private else {".json"})
                        and (include_private or file.name in {"manifest.json", "storyboard.json"})):
                    safe_name = folder.name if include_private else "result_%d" % folder_number
                    add_file(file, "results/" + safe_name + "/" + file.name)
    hashed = 0
    count = 0
    for path in (root / ".studio").rglob("*"):
        if time.monotonic() - started > 20:
            inventory.append({"warning": "清单扫描已到时间上限，文件列表为快照"})
            break
        if not path.is_file() or path.is_symlink():
            continue
        count += 1
        if count > 75000:
            inventory.append({"warning": "仅列出前 75000 个文件"})
            break
        try:
            stat = path.stat()
            detail = {"path": path.relative_to(root).as_posix() if include_private else
                      "file_%d%s" % (count, path.suffix.lower()), "bytes": stat.st_size,
                      "mtime": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()}
            if stat.st_size < 256 * 1024 and hashed < 24 * 1024 * 1024:
                detail["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                hashed += stat.st_size
            inventory.append(detail)
        except OSError as error:
            inventory.append({"file_index": count, "error": str(error) if include_private else type(error).__name__})
    diagnostic = system_report(root, request)
    diagnostic["last_job"] = str(last_job) if last_job else None
    diagnostic["inventory_count"] = len(inventory)
    diagnostic["snapshot_running"] = bool(jobpath and read_json(jobpath / "job.json", {}).get("status") == "运行中")
    if jobpath and jobpath.is_dir():
        checkpoints = sorted(jobpath.glob("scene_*.json"))
        completed = sum(read_json(item, {}).get("passed") is True for item in checkpoints)
        diagnostic["last_job_checkpoints"] = {"count": len(checkpoints), "passed": completed,
                                               "final_reviews": len(read_json(jobpath / "final_reviews.json", []))}
    diagnostic["source_sha256"] = hashlib.sha256(script.read_bytes()).hexdigest()
    with RUNNING_CHILDREN_LOCK:
        active = [proc for proc in RUNNING_CHILDREN if proc.poll() is None]
    diagnostic["child_processes"] = {"count": len(active),
                                      "pids": [proc.pid for proc in active] if include_private else []}
    log_events = []
    recent_lines = []
    if app_log.is_file():
        try:
            with app_log.open("r", encoding="utf-8", errors="replace") as stream:
                recent = deque(stream, maxlen=5000)
            recent_lines = list(recent)
            log_events = diagnostic_log_events(recent_lines)
            diagnostic["log_statistics"] = {"recent_lines": len(recent),
                                            "error_mentions": sum("失败" in line or "Error" in line for line in recent),
                                             "stop_mentions": sum("已停止" in line for line in recent),
                                             "structured_events": len(log_events)}
        except OSError:
            diagnostic["log_statistics"] = {"readable": False}
    stages = []
    latest = read_json(jobpath / "job.json", {}) if jobpath else {}
    for record in latest.get("events", []):
        if not isinstance(record, dict):
            continue
        stages.append({"percent": record.get("percent"),
                       "elapsed_seconds": record.get("elapsed_seconds"),
                       "ram_available": record.get("ram_available"),
                       "gpu_free": record.get("gpu_free"),
                       "disk_free": record.get("disk_free")})
    diagnostic["error_code"] = latest.get("error_code")
    diagnostic["latest_exception"] = diagnostic_exception_summary(latest["error"]) if isinstance(
        latest.get("error"), str) else None
    diagnostic["failed_stage"] = next(({"percent": item.get("percent"), "elapsed_seconds": item.get("elapsed_seconds")}
                                       for item in reversed(latest.get("events", [])) if isinstance(item, dict)), None)
    diagnostic["final_review_failure"] = {key: value for key, value in latest.get("final_review", {}).items()
                                          if key in {"failure_code", "scene", "passed", "review_level"}} if isinstance(
                                              latest.get("final_review"), dict) else {}
    diagnostic["native_verification"] = {key: value for key, value in read_json(
        root / ".studio" / "native_ready.json", {}).items()
        if key in {"offline_load", "inference_tested", "decode_tested", "frame_count", "smoke_status",
                   "smoke_error_type", "smoke_error_code", "gpu_index", "gpu_total_mb"}}
    diagnostic["resource_peak"] = latest.get("resource_report", {})
    diagnostic["repair_attempts"] = len(latest.get("repairs", []))
    diagnostic["repair_outcomes"] = latest.get("repairs", [])
    diagnostic["localized_sources"] = latest.get("localized_sources", {})
    diagnostic["native_review_failures"] = sum(
        len(read_json(item, [])) for item in jobpath.glob("native_attempts_*.json")) if jobpath else 0
    diagnostic["final_audio_review"] = read_json(jobpath / "speech_review.json", []) if jobpath else []
    diagnostic["source_analysis"] = latest.get("source_analysis", [])
    diagnostic["review_summary"] = latest.get("review_summary", {})
    diagnostic["selected_models"] = latest.get("selected_models", {})
    audit_file = root / ".studio" / "logs" / "process_events.jsonl"
    processes = []
    if audit_file.is_file():
        with audit_file.open("r", encoding="utf-8", errors="replace") as handler:
            for line in deque(handler, maxlen=EXTERNAL_COMMAND_HISTORY):
                try:
                    entry = json.loads(line)
                    if isinstance(entry, dict):
                        processes.append(entry if include_private else redact_diagnostic(entry))
                except ValueError:
                    continue
    checkpoint_summary = []
    if jobpath and jobpath.is_dir():
        for file in sorted(jobpath.glob("scene_*.json")):
            item = read_json(file, {})
            visual = item.get("image", {})
            checkpoint_summary.append({"scene": len(checkpoint_summary) + 1,
                                       "passed": item.get("passed"),
                                       "clip_exists": bool(item.get("clip") and Path(item["clip"]).is_file()),
                                       "voice_exists": bool(item.get("voice") and Path(item["voice"]).is_file()),
                                       "image_type": visual.get("type"),
                                       "caption_pages": len(visual.get("overlays", [])),
                                       "semantic_passed": visual.get("metrics", {}).get("passed")
                                       if isinstance(visual.get("metrics"), dict) else None,
                                       "visual_signature_exists": bool(item.get("visual_signature")),
                                       "voice_signature_exists": bool(item.get("voice_signature"))})
    repair_summary = [{"round": item.get("round"), "failure_code": item.get("failure_code"),
                       "at": item.get("at")} for item in latest.get("repairs", []) if isinstance(item, dict)]
    model_progress = []
    for spec in MODEL_SPECS:
        folder = model_path(root, spec[2])
        staging = folder.with_name(folder.name + ".downloading")
        candidate = staging if staging.is_dir() else folder
        if candidate.is_dir():
            count = total = 0
            for file in candidate.rglob("*"):
                try:
                    if file.is_file():
                        count += 1
                        total += file.stat().st_size
                except OSError:
                    continue
            model_progress.append({"model": spec[2], "download_complete": model_download_complete(root, spec),
                                   "saved_file_count": count, "saved_bytes": total})
    if not include_private:
        diagnostic = redact_diagnostic(diagnostic)
    max_total = 140 * 1024 * 1024
    added = 0
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=4, allowZip64=True) as archive:
            archive.writestr("diagnostics/system.json", json.dumps(diagnostic, ensure_ascii=False, indent=2, default=str))
            archive.writestr("diagnostics/file_inventory.json", json.dumps(inventory, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/log_events.json", json.dumps(log_events, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/failure_history.json", json.dumps(
                diagnostic_failure_history(recent_lines, latest, processes), ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/native_verification.json", json.dumps(
                diagnostic.get("native_verification", {}), ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/latest_exception.json", json.dumps(
                diagnostic.get("latest_exception", {}), ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/model_extension.json", json.dumps(
                redact_diagnostic(read_json(root / ".studio" / "native_auto.json", {})),
                ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/process_history.json", json.dumps(processes, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/model_provenance.json", json.dumps(
                model_provenance(root) if include_private else redact_diagnostic(model_provenance(root)),
                ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/stage_metrics.json", json.dumps(stages, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/checkpoint_summary.json", json.dumps(checkpoint_summary, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/repair_summary.json", json.dumps(repair_summary, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/repair_outcomes.json", json.dumps(
                latest.get("repairs", []) if include_private else redact_diagnostic(latest.get("repairs", [])),
                ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/runtime_health.json", json.dumps(
                {"interpreter_matches": runtime_matches_host(root),
                 "basic": packages_healthy(root, "basic"), "full": packages_healthy(root, "full"),
                 "power": system_power_state(), "disk_budget": latest.get("disk_budget", {})},
                ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/model_download_progress.json", json.dumps(model_progress, ensure_ascii=False, indent=2))
            archive.writestr("diagnostics/readme.txt", "诊断包模式：%s。分享前请检查压缩包内容。\n" %
                             ("完整模式：可能包含私人提示词、素材及路径" if include_private else
                              "自动脱敏模式：包含修复、音轨、模型校验等摘要，但不包含原始媒体和输入文本"))
            parts.sort(key=lambda item: (item[0].suffix.lower() not in {".json", ".txt"},
                                         item[0].stat().st_size if item[0].exists() else 0))
            for path, entry in parts:
                try:
                    size = path.stat().st_size
                    if added + size > max_total:
                        omitted.append({"target": entry if include_private else Path(entry).suffix.lower(),
                                        "reason": "archive_size_limit", "bytes": size})
                        continue
                    if not include_private and path.suffix.lower() == ".json":
                        value = read_json(path, None)
                        if value is None:
                            omitted.append({"target": Path(entry).suffix.lower(), "reason": "json_unreadable"})
                            continue
                        archive.writestr(entry, json.dumps(redact_diagnostic(value), ensure_ascii=False,
                                                           indent=2, default=str))
                    else:
                        archive.write(path, arcname=entry)
                    added += size
                except OSError as error:
                    omitted.append({"target": entry if include_private else Path(entry).suffix.lower(),
                                    "reason": type(error).__name__})
            archive.writestr("diagnostics/omissions.json", json.dumps(omitted, ensure_ascii=False, indent=2))
        with zipfile.ZipFile(temporary) as validation:
            damaged = validation.testzip()
            if damaged:
                raise RuntimeError("黑匣子压缩包校验失败，损坏条目：" + damaged)
        if shutil.disk_usage(desktop).free < temporary.stat().st_size + 16 * 1024 * 1024:
            raise RuntimeError("桌面磁盘空间不足，无法安全交付黑匣子")
        shutil.copy2(temporary, desktop_partial)
        with zipfile.ZipFile(desktop_partial) as validation:
            if validation.testzip():
                raise RuntimeError("复制到桌面后的黑匣子校验失败")
        os.replace(desktop_partial, destination)
    finally:
        temporary.unlink(missing_ok=True)
        desktop_partial.unlink(missing_ok=True)
    notifier("黑匣子已保存并校验：" + str(destination))
    return destination


def chinese_duration_number(value):
    text = str(value).strip()
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        return float(text)
    digits = {"零": 0, "〇": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4,
              "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    if not text or not re.fullmatch(r"[零〇一二两三四五六七八九十百]+", text):
        return None
    if all(character in digits for character in text):
        return float(int("".join(str(digits[character]) for character in text)))
    total = current = 0
    for char in text:
        if char in digits:
            current = digits[char]
        elif char == "十":
            total += (current or 1) * 10
            current = 0
        elif char == "百":
            total += (current or 1) * 100
            current = 0
    return float(total + current)


def parse_requested_duration(content):
    content = str(content).lower()
    cn = "零〇一二两三四五六七八九十百"
    number = r"(?:\d{1,4}(?:\.\d+)?|[" + cn + r"]{1,5})"
    colon = re.search(r"(?<!\d)(\d{1,2}):(\d{2})(?!\d)", content)
    patterns = [
        (r"(?<![A-Za-z0-9])(?P<minute>" + number + r")\s*(?:分钟|分)\s*"
         r"(?:(?P<seconds>" + number + r")\s*秒(?:钟)?|(?P<half>半)(?:钟)?)?", "minute"),
        (r"(?<![A-Za-z0-9])半\s*(?:分钟|分)(?:钟)?", "half"),
        (r"(?<![A-Za-z0-9])(?P<seconds>" + number + r")\s*(?:秒(?:钟)?|s\b)", "second")
    ]
    matches = []
    if colon:
        minute, second = int(colon.group(1)), int(colon.group(2))
        if second < 60:
            matches.append((colon.start(), minute * 60 + second))
    for pattern, mode in patterns:
        for result in re.finditer(pattern, content):
            if mode == "half":
                seconds = 30
            elif mode == "minute":
                mins = chinese_duration_number(result.group("minute"))
                extra = chinese_duration_number(result.group("seconds")) if result.group("seconds") else 0
                if mins is None or extra is None:
                    continue
                seconds = mins * 60 + extra + (30 if result.group("half") else 0)
            else:
                seconds = chinese_duration_number(result.group("seconds"))
            if seconds is not None and seconds > 0:
                matches.append((result.start(), seconds))
    return min(matches, key=lambda item: item[0])[1] if matches else None


def recommend_project_settings(prompt, assets, available_memory=0):
    content = re.sub(r"\s+", " ", str(prompt)).strip().lower()
    pictures = sum(len(assets.get(kind, [])) for kind in ("图片", "首帧", "尾帧", "视频"))
    image_count = len(assets.get("图片", [])) + len(assets.get("视频", []))
    if any(word in content for word in ("竖屏", "9:16", "9：16")):
        aspect = "竖屏 9:16"
        aspect_reason = "识别到竖屏需求"
    elif any(word in content for word in ("横屏", "16:9", "16：9", "宽屏")):
        aspect = "横屏 16:9"
        aspect_reason = "识别到宽屏需求"
    elif any(word in content for word in ("方形", "正方形", "1:1", "1：1")):
        aspect = "方形 1:1"
        aspect_reason = "识别到方形构图"
    elif any(word in content for word in ("抖音", "快手", "tiktok", "reels", "shorts", "小红书", "手机短视频")):
        aspect = "竖屏 9:16"
        aspect_reason = "移动端内容推荐竖屏"
    else:
        aspect = "横屏 16:9"
        aspect_reason = "默认电影宽屏构图"
    requested_seconds = parse_requested_duration(content)
    if requested_seconds is not None:
        rounded = math.ceil(requested_seconds)
        bounded = max(6, min(120, rounded))
        duration = str(bounded)
        duration_reason = ("已采用提示词指定的时长" if bounded == rounded else
                           "提示词要求%d秒，已按当前可安全制作的6至120秒范围调整为%d秒" % (rounded, bounded))
    elif any(word in content for word in ("一分钟", "1分钟", "60秒", "完整教程", "长故事", "知识科普")):
        duration = "60"
        duration_reason = "讲解内容需要更完整的叙事"
    elif any(word in content for word in ("预告片", "片头", "闪剪", "15秒", "简短广告")):
        duration = "15"
        duration_reason = "短节奏内容建议15秒"
    elif image_count >= 5:
        duration = "60"
        duration_reason = "素材较多，推荐更充分的镜头时长"
    else:
        duration = "30"
        duration_reason = "推荐30秒创作长度"
    if 0 < available_memory < 4 * GB:
        quality = "快速"
        quality_reason = "可用内存较少，优先降低负载"
    elif (available_memory >= 12 * GB and any(word in content for word in
                                               ("精细", "精致", "高画质", "高品质", "细节丰富"))):
        quality = "精细"
        quality_reason = "画质要求较高，内存条件适合精细模式"
    else:
        quality = "智能"
        quality_reason = "自动平衡画质和设备负载"
    role = "仅作参考"
    if assets.get("音频") and any(word in content for word in
                                    ("背景音乐", "作为配乐", "使用上传的音乐", "用我的音乐", "用上传的音乐")):
        role = "作为背景音乐"
    reasons = [aspect_reason, duration_reason, quality_reason]
    if pictures and not content:
        reasons = ["已识别 %d 份画面素材" % pictures, duration_reason, quality_reason]
    if role == "作为背景音乐":
        reasons.append("已建议采用上传的背景音乐")
    return {"aspect": aspect, "duration": duration, "quality": quality,
            "audio_role": role, "reasons": reasons}

class StudioUI:
    def __init__(self):
        import tkinter as tk
        from tkinter import filedialog, messagebox, ttk
        self.tk = tk
        self.ttk = ttk
        self.filedialog = filedialog
        self.messagebox = messagebox
        if os.name == "nt":
            try:
                try:
                    ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
                except (AttributeError, OSError, ValueError):
                    ctypes.windll.shcore.SetProcessDpiAwareness(2)
            except (OSError, AttributeError):
                pass
        self.root = tk.Tk()
        if os.name == "nt":
            try:
                dpi = int(ctypes.windll.user32.GetDpiForWindow(self.root.winfo_id()))
                if dpi > 0:
                    self.root.tk.call("tk", "scaling", dpi / 72.0)
            except (OSError, AttributeError, ValueError, tk.TclError):
                pass
        self.root.title(APP_NAME)
        self.last_dpi = None
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        usable_width = max(480, screen_width - 56)
        usable_height = max(420, screen_height - 86)
        min_width = min(720, usable_width)
        min_height = min(550, usable_height)
        self.root.minsize(min_width, min_height)
        width = max(min_width, min(1280, int(screen_width * .89), usable_width))
        height = max(min_height, min(920, int(screen_height * .88), usable_height))
        self.root.geometry("%dx%d+%d+%d" % (width, height, max(0, (screen_width - width) // 2),
                                             max(0, (screen_height - height) // 2)))
        self.palette = {
            "bg": "#090F1B", "panel": "#111B2B", "surface": "#172336", "input": "#0D1727",
            "stroke": "#27374D", "fg": "#F0F5FE", "muted": "#91A5BE", "accent": "#58B3FF",
            "accent_bg": "#1466BB", "accent_hover": "#237DCE", "green": "#66DFBA",
            "amber": "#F3C674", "danger": "#FF9295", "soft": "#B7C8DD"
        }
        self.font_family = "Microsoft YaHei UI" if os.name == "nt" else "DejaVu Sans"
        self.root.configure(bg=self.palette["bg"])
        self.root_path = None
        self.workspace_lock = None
        self.task = None
        self.ready = False
        self.blackbox_active = False
        self.stop_event = threading.Event()
        self.install_stop = threading.Event()
        self.setup_active = False
        self.basic_ready = False
        self.capabilities = {}
        self.setup_thread = None
        self.native_auto_thread = None
        self.native_stop = threading.Event()
        self.deployment_retry = 0
        self.force_integrity_scan = False
        self.pending_start_request = None
        self.job_stop_file = None
        self.events = queue.Queue()
        self.log_lock = threading.Lock()
        self.assets = {name: [] for name in ("图片", "首帧", "尾帧", "音频", "视频", "文档")}
        self.last_job = None
        self.last_output = None
        self.recommendation_after = None
        self.current_phase = "idle"
        self.scene_entries = []
        self.scene_rows = []
        self.preview_file = None
        self.preview_photo = None
        self.wide_layout = None
        self.setup_ui()
        self.tune_native_window()
        self.root.after(120, self.process_events)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(250, self.select_workspace)

    def tune_native_window(self):
        if os.name != "nt":
            return
        try:
            parent_function = ctypes.windll.user32.GetParent
            parent_function.argtypes = [ctypes.c_void_p]
            parent_function.restype = ctypes.c_void_p
            handle = parent_function(self.root.winfo_id()) or self.root.winfo_id()
            theme_function = ctypes.windll.dwmapi.DwmSetWindowAttribute
            theme_function.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
            theme_function.restype = ctypes.c_long
            dark = ctypes.c_int(1)
            rounded = ctypes.c_int(2)
            theme_function(handle, 20, ctypes.byref(dark), ctypes.sizeof(dark))
            theme_function(handle, 33, ctypes.byref(rounded), ctypes.sizeof(rounded))
        except (OSError, AttributeError, ValueError):
            pass

    def label(self, parent, text, size=10, color=None, strong=False, bg=None, **kwargs):
        return self.tk.Label(parent, text=text, bg=bg or self.palette["panel"],
                             fg=color or self.palette["fg"], anchor="w", justify="left",
                             font=(self.font_family, size, "bold" if strong else "normal"), **kwargs)

    def card(self, parent, padx=18, pady=17):
        return self.tk.Frame(parent, bg=self.palette["panel"], padx=padx, pady=pady,
                             bd=0, highlightthickness=1, highlightbackground=self.palette["stroke"])

    def setup_ui(self):
        tk = self.tk
        ttk = self.ttk
        p = self.palette
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", background=p["surface"], foreground=p["fg"],
                        borderwidth=0, relief="flat", padding=(12, 9),
                        font=(self.font_family, 10))
        style.map("TButton", background=[("active", "#243A55"), ("disabled", "#1A2739")],
                  foreground=[("disabled", "#6F849D")])
        style.configure("Primary.TButton", background=p["accent_bg"], foreground="#FFFFFF",
                        borderwidth=0, relief="flat", padding=(23, 12),
                        font=(self.font_family, 11, "bold"))
        style.map("Primary.TButton", background=[("active", p["accent_hover"]),
                                                  ("disabled", "#273A50")],
                  foreground=[("disabled", "#8497AC")])
        style.configure("Small.TButton", background=p["surface"], foreground=p["soft"],
                        borderwidth=0, padding=(10, 6), font=(self.font_family, 9))
        style.map("Small.TButton", background=[("active", "#263A55"), ("disabled", "#1A2739")],
                  foreground=[("disabled", "#70859E")])
        style.configure("Modern.TCombobox", fieldbackground=p["input"], background=p["input"],
                        foreground=p["fg"], arrowcolor=p["soft"], borderwidth=0, relief="flat",
                        selectbackground=p["accent_bg"], selectforeground="white", padding=8,
                        font=(self.font_family, 10))
        style.map("Modern.TCombobox", fieldbackground=[("readonly", p["input"])],
                  foreground=[("readonly", p["fg"])],
                  selectbackground=[("readonly", p["input"])],
                  selectforeground=[("readonly", p["fg"])])
        style.configure("Slim.Horizontal.TProgressbar", troughcolor=p["stroke"],
                        background=p["accent"], bordercolor=p["stroke"],
                        lightcolor=p["accent"], darkcolor=p["accent"], thickness=6)
        style.configure("Vertical.TScrollbar", background=p["surface"], troughcolor=p["bg"],
                        bordercolor=p["bg"], arrowcolor=p["muted"])
        self.header = tk.Frame(self.root, bg=p["bg"], padx=25, pady=16)
        self.header.pack(fill="x")
        brand = tk.Frame(self.header, bg=p["bg"])
        brand.pack(side="left")
        mark = tk.Canvas(brand, width=41, height=41, bg=p["bg"], highlightthickness=0)
        mark.pack(side="left", padx=(0, 12))
        mark.create_rectangle(2, 2, 39, 39, fill=p["accent_bg"], outline=p["accent_bg"], width=0)
        mark.create_text(20, 20, text="AI", fill="#FFFFFF", font=("Segoe UI", 13, "bold"))
        brand_text = tk.Frame(brand, bg=p["bg"])
        brand_text.pack(side="left")
        self.label(brand_text, "AI 视频工坊", 16, strong=True, bg=p["bg"]).pack(anchor="w")
        tools = tk.Frame(self.header, bg=p["bg"])
        tools.pack(side="right")
        self.ready_badge = self.label(tools, "● 尚未就绪", 10, p["muted"], bg=p["bg"])
        self.ready_badge.pack(side="left", padx=(0, 16))
        ttk.Button(tools, text="工作目录", style="Small.TButton",
                   command=self.select_workspace).pack(side="left")
        status_bar = tk.Frame(self.root, bg=p["panel"], padx=25, pady=10,
                              highlightbackground=p["stroke"], highlightthickness=1)
        status_bar.pack(fill="x", padx=20, pady=(0, 5))
        state_row = tk.Frame(status_bar, bg=p["panel"])
        state_row.pack(fill="x")
        self.stage_label = self.label(state_row, "准备离线环境", 9,
                                      p["soft"], bg=p["panel"], wraplength=850)
        self.stage_label.pack(side="left", fill="x", expand=True)
        self.folder_label = self.label(status_bar, "尚未选择工作目录", 8, p["muted"],
                                       bg=p["panel"], wraplength=850)
        self.folder_label.pack(fill="x", pady=(3, 4))
        self.capability_label = self.label(status_bar, "离线能力检测中", 9,
                                           p["soft"], bg=p["panel"], wraplength=850)
        self.capability_label.pack(fill="x", pady=(0, 5))
        self.setup_progress = ttk.Progressbar(status_bar, style="Slim.Horizontal.TProgressbar",
                                               mode="determinate", maximum=100)
        self.setup_progress.pack(fill="x")
        outer = tk.Frame(self.root, bg=p["bg"])
        outer.pack(fill="both", expand=True)
        self.main_canvas = tk.Canvas(outer, bg=p["bg"], highlightthickness=0, bd=0)
        scrolling = ttk.Scrollbar(outer, orient="vertical", command=self.main_canvas.yview)
        self.main_canvas.configure(yscrollcommand=scrolling.set)
        scrolling.pack(side="right", fill="y")
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.body = tk.Frame(self.main_canvas, bg=p["bg"], padx=20, pady=16)
        self.body_window = self.main_canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.main_canvas.bind("<Configure>", self.main_canvas_resized)
        self.body.bind("<Configure>", lambda event: self.root.after_idle(self.refresh_scrollregion))
        self.root.bind_all("<MouseWheel>", self.scroll_workspace)
        self.root.bind_all("<Button-4>", self.scroll_workspace)
        self.root.bind_all("<Button-5>", self.scroll_workspace)
        self.columns = tk.Frame(self.body, bg=p["bg"])
        self.columns.pack(fill="x")
        self.creation_column = self.build_creation_panel(self.columns)
        self.preview_column = self.build_preview_panel(self.columns)
        self.apply_responsive_layout(self.root.winfo_width())
        self.footer = tk.Frame(self.root, bg=p["bg"], padx=23, pady=13)
        self.footer.pack(fill="x")
        self.start_btn = ttk.Button(self.footer, text="启动", style="Primary.TButton",
                                    command=self.start_job)
        self.start_btn.pack(side="left", padx=(0, 9))
        self.black_btn = ttk.Button(self.footer, text="黑匣子", style="Small.TButton", command=self.blackbox)
        self.black_btn.pack(side="right", padx=(8, 0))
        self.open_btn = ttk.Button(self.footer, text="打开成品目录", style="Small.TButton",
                                   command=self.open_output)
        self.open_btn.pack(side="right")
        self.refresh_asset_label()
        self.refresh_smart_suggestions()
        self.render_task_state("idle")
        self.refresh_buttons()

    def build_creation_panel(self, parent):
        tk = self.tk
        ttk = self.ttk
        p = self.palette
        column = tk.Frame(parent, bg=p["bg"])
        hero = tk.Frame(column, bg=p["bg"])
        hero.pack(fill="x", pady=(2, 15))
        self.label(hero, "从一个想法，开始创作", 20, strong=True, bg=p["bg"]).pack(anchor="w")
        self.label(hero, "输入你希望最终视频呈现的内容", 10,
                   p["muted"], bg=p["bg"]).pack(anchor="w", pady=(4, 0))
        prompt_card = self.card(column)
        prompt_card.pack(fill="x", pady=(0, 12))
        header = tk.Frame(prompt_card, bg=p["panel"])
        header.pack(fill="x", pady=(0, 10))
        self.label(header, "01  创作灵感", 11, strong=True).pack(side="left")

        self.prompt_box = tk.Text(prompt_card, height=6, wrap="word", undo=True, relief="flat", bd=0,
                                  background=p["input"], foreground=p["fg"], insertbackground=p["fg"],
                                  selectbackground=p["accent_bg"], selectforeground="white",
                                  font=(self.font_family, 11), padx=14, pady=13,
                                  highlightthickness=1, highlightbackground=p["stroke"],
                                  highlightcolor=p["accent"])
        self.prompt_box.pack(fill="x")
        self.prompt_box.insert("1.0", "例：制作一段温暖的城市夜景短片，镜头有电影感，配中文旁白。")
        self.prompt_box.bind("<FocusIn>", self.clear_example)
        self.prompt_box.bind("<KeyRelease>", self.schedule_recommendations)
        asset_card = self.card(column)
        asset_card.pack(fill="x", pady=(0, 12))
        file_head = tk.Frame(asset_card, bg=p["panel"])
        file_head.pack(fill="x")
        self.label(file_head, "02  参考素材", 11, strong=True).pack(side="left")
        ttk.Button(file_head, text="＋ 添加素材", style="Small.TButton",
                   command=self.add_assets).pack(side="right")
        self.assets_label = self.label(asset_card, "尚未添加素材", 9, p["muted"])
        self.assets_label.pack(anchor="w", pady=(9, 7))
        self.asset_rows_frame = tk.Frame(asset_card, bg=p["panel"])
        self.asset_rows_frame.pack(fill="x")
        file_action = tk.Frame(asset_card, bg=p["panel"])
        file_action.pack(fill="x", pady=(8, 0))
        ttk.Button(file_action, text="指定首尾帧 / 管理", style="Small.TButton",
                   command=self.manage_assets).pack(side="left")
        config_card = self.card(column)
        config_card.pack(fill="x")
        self.label(config_card, "自动视频方案", 10, p["soft"], strong=True).pack(anchor="w")
        self.duration = tk.StringVar(value="30")
        self.quality = tk.StringVar(value="智能")
        self.aspect = tk.StringVar(value="横屏 16:9")
        self.audio_role = tk.StringVar(value="仅作参考")
        self.source_audio_role = tk.StringVar(value="自动混合原声")
        self.visual_mode = tk.StringVar(value="智能轻量运镜")
        self.recommendation_label = self.label(config_card, "分析中", 10,
                                               p["green"], wraplength=520)
        self.recommendation_label.pack(anchor="w", fill="x", pady=(8, 0))
        return column

    def build_preview_panel(self, parent):
        tk = self.tk
        ttk = self.ttk
        p = self.palette
        column = tk.Frame(parent, bg=p["bg"])
        self.label(column, "创作监视器", 13, strong=True, bg=p["bg"]).pack(anchor="w", pady=(5, 12))
        preview_card = self.card(column, 14, 14)
        preview_card.pack(fill="x", pady=(0, 12))
        preview_header = tk.Frame(preview_card, bg=p["panel"])
        preview_header.pack(fill="x", pady=(0, 10))
        self.label(preview_header, "画面预览", 10, strong=True).pack(side="left")
        self.preview_state = self.label(preview_header, "等待创作", 9, p["muted"])
        self.preview_state.pack(side="right")
        self.preview_canvas = tk.Canvas(preview_card, height=240, bg=p["input"],
                                        highlightthickness=1, highlightbackground=p["stroke"], bd=0)
        self.preview_canvas.pack(fill="x")
        self.preview_canvas.bind("<Configure>", self.draw_preview)
        self.preview_caption = self.label(preview_card, "分镜完成后，画面会逐幕出现在这里", 9,
                                           p["muted"], wraplength=390)
        self.preview_caption.pack(fill="x", pady=(10, 0))
        flow_card = self.card(column, 14, 14)
        flow_card.pack(fill="x", pady=(0, 12))
        progress_head = tk.Frame(flow_card, bg=p["panel"])
        progress_head.pack(fill="x")
        self.label(progress_head, "任务进度", 10, strong=True).pack(side="left")
        self.progress_text = self.label(progress_head, "0%", 10, p["accent"], strong=True)
        self.progress_text.pack(side="right")
        self.creation_progress = ttk.Progressbar(flow_card, style="Slim.Horizontal.TProgressbar",
                                                 mode="determinate", maximum=100)
        self.creation_progress.pack(fill="x", pady=(12, 13))
        self.phase_widgets = {}
        for phase, title in (("preparing", "准备素材"), ("planning", "理解需求与分镜规划"),
                             ("rendering", "生成、审校与修复镜头"), ("finishing", "剪辑、混音与成片校验")):
            line = tk.Frame(flow_card, bg=p["panel"])
            line.pack(fill="x", pady=(0, 8))
            marker = self.label(line, "○", 12, p["muted"])
            marker.pack(side="left", padx=(0, 9))
            name_label = self.label(line, title, 9, p["muted"])
            name_label.pack(side="left", fill="x", expand=True)
            self.phase_widgets[phase] = (marker, name_label)
        scene_card = self.card(column, 14, 14)
        scene_card.pack(fill="x", pady=(0, 12))
        scene_header = tk.Frame(scene_card, bg=p["panel"])
        scene_header.pack(fill="x")
        self.label(scene_header, "镜头时间线", 10, strong=True).pack(side="left")
        self.scene_count = self.label(scene_header, "待规划", 9, p["muted"])
        self.scene_count.pack(side="right")
        self.scene_rows_frame = tk.Frame(scene_card, bg=p["panel"])
        self.scene_rows_frame.pack(fill="x", pady=(10, 0))
        self.scene_empty_label = self.label(self.scene_rows_frame, "AI 完成分镜规划后，将显示各幕进度", 9,
                                            p["muted"], wraplength=340)
        self.scene_empty_label.pack(anchor="w")
        self.result_card = self.card(column, 14, 14)
        self.label(self.result_card, "作品已完成", 12, p["green"], strong=True).pack(anchor="w")
        self.result_info = self.label(self.result_card, "", 9, p["soft"], wraplength=360)
        self.result_info.pack(fill="x", pady=(9, 10))
        return column

    def main_canvas_resized(self, event):
        self.main_canvas.itemconfigure(self.body_window, width=event.width)
        self.apply_responsive_layout(event.width)
        if os.name == "nt":
            try:
                dpi = int(ctypes.windll.user32.GetDpiForWindow(self.root.winfo_id()))
                if dpi > 0 and dpi != self.last_dpi:
                    self.last_dpi = dpi
                    self.root.tk.call("tk", "scaling", dpi / 72.0)
            except (OSError, AttributeError, ValueError, self.tk.TclError):
                pass
        wrap_width = max(190, event.width - max(35, int(self.root.winfo_fpixels("0.65i"))))
        self.folder_label.configure(wraplength=wrap_width)
        self.stage_label.configure(wraplength=wrap_width)
        self.recommendation_label.configure(wraplength=max(170, int(event.width * (.40 if self.wide_layout else .82))))
        if hasattr(self, "scene_rows"):
            available = max(130, int(event.width * (.25 if self.wide_layout else .65)))
            for marker, content, state in self.scene_rows:
                content.configure(wraplength=available)
        self.root.after_idle(self.refresh_scrollregion)

    def apply_responsive_layout(self, width):
        min_panel_width = max(320, int(self.root.winfo_fpixels("4.2i")))
        min_preview_width = max(280, int(self.root.winfo_fpixels("3.6i")))
        wide = width >= min_panel_width + min_preview_width + max(25, int(self.root.winfo_fpixels("0.5i")))
        if wide == self.wide_layout:
            return
        self.wide_layout = wide
        self.creation_column.grid_forget()
        self.preview_column.grid_forget()
        if wide:
            self.columns.grid_columnconfigure(0, weight=3)
            self.columns.grid_columnconfigure(1, weight=2)
            self.creation_column.grid(row=0, column=0, sticky="new", padx=(0, 13))
            self.preview_column.grid(row=0, column=1, sticky="new")
        else:
            self.columns.grid_columnconfigure(0, weight=1)
            self.columns.grid_columnconfigure(1, weight=0)
            self.creation_column.grid(row=0, column=0, sticky="new")
            self.preview_column.grid(row=1, column=0, sticky="new", pady=(14, 0))
        self.root.after_idle(self.refresh_scrollregion)

    def refresh_scrollregion(self):
        try:
            region = self.main_canvas.bbox("all")
            if region is not None:
                self.main_canvas.configure(scrollregion=region)
        except self.tk.TclError:
            pass

    def scroll_workspace(self, event):
        try:
            if event.widget.winfo_toplevel() != self.root:
                return
            if isinstance(event.widget, (self.tk.Text, self.tk.Listbox, self.ttk.Combobox)) or \
                    event.widget.winfo_class() in {"Text", "Listbox", "TCombobox", "Treeview"}:
                return
            step = -1 if getattr(event, "delta", 0) > 0 or getattr(event, "num", None) == 4 else 1
            self.main_canvas.yview_scroll(step * 2, "units")
        except self.tk.TclError:
            pass

    def schedule_recommendations(self, event=None):
        if self.recommendation_after is not None:
            self.root.after_cancel(self.recommendation_after)
        self.recommendation_after = self.root.after(UI_RECOMMEND_DELAY_MS, self.refresh_smart_suggestions)

    def refresh_smart_suggestions(self):
        self.recommendation_after = None
        if not hasattr(self, "recommendation_label"):
            return
        prompt = self.prompt_box.get("1.0", "end-1c").strip()
        if prompt.startswith("例："):
            prompt = ""
        proposal = recommend_project_settings(prompt, self.assets, memory_info()["available"])
        for key, variable in (("duration", self.duration), ("aspect", self.aspect),
                              ("quality", self.quality), ("audio_role", self.audio_role)):
            variable.set(str(proposal[key]))
        available = self.capabilities.get("native_video", False)
        self.visual_mode.set("原生AI视频（自动）" if available else "智能轻量运镜")
        plan = ("%s 秒 · %s · %s画质" % (self.duration.get(), self.aspect.get(), self.quality.get()))
        if self.assets["音频"] and self.audio_role.get() == "作为背景音乐":
            plan += " · 采用提供的配乐"
        if self.assets["视频"]:
            self.source_audio_role.set("自动混合原声")
        if available:
            plan += " · 优先原生动态，未通过审校时自动改用图片运镜"
        elif self.capabilities.get("full_offline"):
            plan += " · AI 图片动态运镜"
        else:
            plan += " · 离线模型准备中"
        self.recommendation_label.configure(text=plan)

    def draw_preview(self, event=None):
        canvas = self.preview_canvas
        canvas.delete("all")
        width = max(1, canvas.winfo_width())
        height = max(1, canvas.winfo_height())
        if self.preview_file and Path(self.preview_file).is_file():
            try:
                photo = self.tk.PhotoImage(file=str(self.preview_file))
                stride = max(1, math.ceil(max(photo.width() / width, photo.height() / height)))
                if stride > 1:
                    photo = photo.subsample(stride, stride)
                self.preview_photo = photo
                canvas.create_image(width // 2, height // 2, image=photo)
                return
            except (self.tk.TclError, OSError, ValueError):
                self.preview_photo = None
        canvas.create_oval(width // 2 - 28, height // 2 - 44, width // 2 + 28,
                           height // 2 + 12, outline=self.palette["stroke"], width=2)
        canvas.create_polygon(width // 2 - 5, height // 2 - 31, width // 2 + 15, height // 2 - 16,
                              width // 2 - 5, height // 2 - 1, fill=self.palette["muted"])
        canvas.create_text(width // 2, height // 2 + 42, text="等待第一幕画面", fill=self.palette["muted"],
                           font=(self.font_family, 10))

    def show_preview(self, filepath, caption=""):
        file = Path(filepath) if filepath else None
        if file and file.is_file() and file.suffix.lower() in {".png", ".gif", ".ppm", ".pgm"}:
            self.preview_file = str(file)
        else:
            self.preview_file = None
        if caption:
            self.preview_caption.configure(text=caption)
        self.draw_preview()

    def render_storyboard(self, title, scenes):
        tk = self.tk
        p = self.palette
        self.scene_entries = [dict(scene, state="pending") for scene in scenes[:UI_MAX_SCENE_ROWS]]
        self.scene_count.configure(text="%d 幕" % len(self.scene_entries))
        for child in self.scene_rows_frame.winfo_children():
            child.destroy()
        self.scene_rows = []
        for index, scene in enumerate(self.scene_entries):
            item = tk.Frame(self.scene_rows_frame, bg=p["surface"], padx=10, pady=9)
            item.pack(fill="x", pady=(0, 6))
            marker = self.label(item, "%02d" % (index + 1), 10, p["muted"], strong=True,
                                bg=p["surface"])
            marker.pack(side="left", padx=(0, 11))
            text = self.label(item, str(scene.get("narration", "待生成"))[:48], 9,
                              p["soft"], bg=p["surface"], wraplength=230)
            text.pack(side="left", fill="x", expand=True)
            state = self.label(item, "待生成", 8, p["muted"], bg=p["surface"])
            state.pack(side="right", padx=(5, 0))
            self.scene_rows.append((marker, text, state))
        self.preview_caption.configure(text=title or "开始制作分镜")

    def render_scene_state(self, index, state, preview=None, review=""):
        if index < 0 or index >= len(self.scene_entries):
            return
        self.scene_entries[index]["state"] = state
        marker, text, indicator = self.scene_rows[index]
        if state == "active":
            marker.configure(fg=self.palette["accent"])
            text.configure(fg=self.palette["fg"])
            indicator.configure(text="生成中", fg=self.palette["accent"])
            self.preview_state.configure(text="第 %d 幕生成中" % (index + 1), fg=self.palette["accent"])
        elif state == "reviewing":
            marker.configure(fg=self.palette["accent"])
            indicator.configure(text="AI 审校中", fg=self.palette["accent"])
            self.preview_state.configure(text="第 %d 幕审校中" % (index + 1), fg=self.palette["accent"])
        elif state == "done":
            uncertain = any(flag in review for flag in ("unreviewed", "supplied_conflict", "not_checked"))
            color = self.palette["amber"] if uncertain else self.palette["green"]
            marker.configure(fg=color)
            text.configure(fg=self.palette["soft"])
            indicator.configure(text="! 未获语义通过" if uncertain else "✓ 已通过", fg=color)
            self.preview_state.configure(text="镜头 %d 已完成 · %s" % (
                index + 1, "部分检查未通过" if uncertain else "审校通过"), fg=color)
            if preview:
                self.show_preview(preview, "第 %d 幕 · %s" % (index + 1, review or "检查完成"))

    def render_task_state(self, phase):
        order = ("preparing", "planning", "rendering", "finishing")
        self.current_phase = phase
        current = order.index(phase) if phase in order else (-1 if phase == "idle" else len(order))
        for index, key in enumerate(order):
            marker, label = self.phase_widgets[key]
            if index < current:
                marker.configure(text="✓", fg=self.palette["green"])
                label.configure(fg=self.palette["soft"])
            elif index == current:
                marker.configure(text="●", fg=self.palette["accent"])
                label.configure(fg=self.palette["fg"])
            else:
                marker.configure(text="○", fg=self.palette["muted"])
                label.configure(fg=self.palette["muted"])
        if phase == "complete":
            self.preview_state.configure(text="创作完成", fg=self.palette["green"])
        elif phase == "idle":
            self.preview_state.configure(text="等待创作", fg=self.palette["muted"])

    def show_result_panel(self, output):
        self.result_card.pack(fill="x", pady=(0, 12))
        self.result_card.winfo_children()[0].configure(text="作品已完成", fg=self.palette["green"])
        data = read_json(output.parent / "manifest.json", {})
        width, height = (data.get("resolution") or [0, 0])[:2]
        seconds = data.get("duration", 0)
        scenes = data.get("scene_count", len(self.scene_entries))
        text = "%s × %s  ·  %.1f 秒  ·  %s 幕\n%s" % (
            width or "?", height or "?", float(seconds), scenes, output.name)
        warnings = data.get("warnings") or []
        if warnings:
            text += "\n提醒：" + str(warnings[0])[:120]
        self.result_info.configure(text=text)
        cover = output.parent / "cover.png"
        if cover.is_file():
            self.show_preview(cover, "成片封面 · 已完成技术校验")

    def show_job_error(self, message):
        self.result_card.pack(fill="x", pady=(0, 12))
        self.result_card.winfo_children()[0].configure(text="任务未完成", fg=self.palette["danger"])
        self.result_info.configure(text=str(message)[:280] + "\n可使用黑匣子保存脱敏故障报告。")
        self.preview_state.configure(text="需要处理", fg=self.palette["danger"])

    def clear_example(self, event):
        current = self.prompt_box.get("1.0", "end-1c").strip()
        if current.startswith("例："):
            self.prompt_box.delete("1.0", "end")

    def add_assets(self):
        if self.task not in (None, "部署") or self.blackbox_active:
            return
        patterns = ("*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff "
                    "*.wav *.mp3 *.flac *.m4a *.aac *.ogg *.wma "
                    "*.mp4 *.mov *.mkv *.avi *.webm *.m4v "
                    "*.txt *.md *.csv *.json *.pdf *.docx *.html *.htm *.srt")
        selected = self.filedialog.askopenfilenames(title="选择图片、视频、音频或文档",
                                                    filetypes=[("支持的素材", patterns), ("所有文件", "*.*")])
        if not selected:
            return
        ignored = []
        for filename in selected:
            extension = Path(filename).suffix.lower()
            if extension in IMAGE_TYPES:
                kind = "图片"
            elif extension in VIDEO_TYPES:
                kind = "视频"
            elif extension in AUDIO_TYPES:
                kind = "音频"
            elif extension in DOC_TYPES:
                kind = "文档"
            else:
                ignored.append(Path(filename).name)
                continue
            if filename not in self.assets[kind] and filename not in self.assets["首帧"] + self.assets["尾帧"]:
                self.assets[kind].append(filename)
        self.refresh_asset_label()
        if ignored:
            self.messagebox.showwarning(APP_NAME, "部分文件格式未被支持：\n" + "、".join(ignored[:5]))

    def refresh_asset_label(self):
        if not hasattr(self, "asset_rows_frame"):
            return
        for widget in self.asset_rows_frame.winfo_children():
            widget.destroy()
        entries = [(kind, file) for kind, paths in self.assets.items() for file in paths]
        total = len(entries)
        self.assets_label.configure(text="已添加 %d 份素材 · 可继续补充" % total if total else
                                    "可选：图片、视频、音频、文档，也可以指定首尾帧")
        if not total:
            empty = self.label(self.asset_rows_frame, "尚未添加参考素材", 9,
                               self.palette["muted"])
            empty.pack(anchor="w", pady=(2, 1))
        icons = {"首帧": "▣", "尾帧": "▣", "图片": "▧", "视频": "▶", "音频": "♫", "文档": "▤"}
        for kind, filename in entries[:UI_MAX_ASSET_ROWS]:
            row = self.tk.Frame(self.asset_rows_frame, bg=self.palette["surface"], padx=9, pady=7)
            row.pack(fill="x", pady=(0, 5))
            self.label(row, icons.get(kind, "●"), 11, self.palette["accent"],
                       bg=self.palette["surface"]).pack(side="left", padx=(0, 9))
            title = Path(filename).name
            self.label(row, title if len(title) <= 34 else title[:16] + "…" + title[-14:], 9,
                       self.palette["soft"], bg=self.palette["surface"]).pack(side="left", fill="x", expand=True)
            self.label(row, kind, 8, self.palette["muted"],
                       bg=self.palette["surface"]).pack(side="right", padx=(8, 0))
        if total > UI_MAX_ASSET_ROWS:
            self.label(self.asset_rows_frame, "还有 %d 份素材 · 点击上方管理按钮查看" %
                       (total - UI_MAX_ASSET_ROWS), 9, self.palette["muted"]).pack(anchor="w", pady=(3, 0))
        if hasattr(self, "recommendation_label"):
            self.schedule_recommendations()

    def manage_assets(self):
        if self.task not in (None, "部署") or self.blackbox_active:
            return
        entries = [(kind, file) for kind, paths in self.assets.items() for file in paths]
        if not entries:
            self.add_assets()
            return
        dialog = self.tk.Toplevel(self.root)
        dialog.title("管理参考素材")
        dialog.transient(self.root)
        dialog.configure(bg=self.palette["panel"])
        dialog.geometry("%dx%d" % (min(720, max(430, self.root.winfo_width() - 160)),
                                     min(460, max(320, self.root.winfo_height() - 170))))
        self.label(dialog, "素材清单", 13, strong=True).pack(anchor="w", padx=16, pady=(14, 8))
        picker = self.tk.Listbox(dialog, selectmode="extended", exportselection=False, borderwidth=0,
                                 highlightthickness=1, highlightbackground=self.palette["stroke"],
                                 bg=self.palette["input"], fg=self.palette["fg"],
                                 selectbackground=self.palette["accent_bg"],
                                 font=(self.font_family, 10), activestyle="none")
        picker.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        def populate():
            entries[:] = [(kind, file) for kind, paths in self.assets.items() for file in paths]
            picker.delete(0, "end")
            for kind, filename in entries:
                picker.insert("end", "[%s]  %s" % (kind, Path(filename).name))
        def remove_selected():
            for index in sorted(picker.curselection(), reverse=True):
                kind, file = entries[index]
                self.assets[kind].remove(file)
            populate()
            self.refresh_asset_label()
        def set_boundary(which):
            selected = picker.curselection()
            if len(selected) != 1:
                self.messagebox.showinfo(APP_NAME, "请先选中一张图片")
                return
            kind, file = entries[selected[0]]
            if Path(file).suffix.lower() not in IMAGE_TYPES:
                self.messagebox.showinfo(APP_NAME, "首帧和尾帧只能指定图片")
                return
            previous = list(self.assets[which])
            if file in self.assets["图片"]:
                self.assets["图片"].remove(file)
            self.assets[which] = [file]
            if previous and previous[0] != file:
                old = previous[0]
                if old not in self.assets["图片"] and old not in self.assets["首帧"] + self.assets["尾帧"]:
                    self.assets["图片"].append(old)
            populate()
            self.refresh_asset_label()
        actions = self.tk.Frame(dialog, bg=self.palette["panel"])
        actions.pack(fill="x", padx=16, pady=(0, 15))
        self.ttk.Button(actions, text="设为首帧", style="Small.TButton",
                        command=lambda: set_boundary("首帧")).pack(side="left", padx=(0, 7))
        self.ttk.Button(actions, text="设为尾帧", style="Small.TButton",
                        command=lambda: set_boundary("尾帧")).pack(side="left", padx=(0, 7))
        self.ttk.Button(actions, text="移除选中", style="Small.TButton",
                        command=remove_selected).pack(side="left")
        self.ttk.Button(actions, text="完成", style="Small.TButton",
                        command=dialog.destroy).pack(side="right")
        populate()
        dialog.grab_set()

    def select_workspace(self):
        if (self.task or self.blackbox_active or self.setup_active or
                (self.native_auto_thread is not None and self.native_auto_thread.is_alive())):
            self.messagebox.showinfo(APP_NAME, "后台正在处理模型或任务，暂不能切换工作目录")
            return
        selected = self.filedialog.askdirectory(title="请选择保存模型、素材和成品的文件夹", mustexist=True)
        if not selected:
            if not self.root_path:
                self.set_status("请选择工作目录才能开始")
            return
        root = Path(selected).resolve()
        if root == self.root_path:
            self.update_setup()
            return
        if os.name == "nt" and len(str(root)) + MIN_WORKSPACE_PATH_MARGIN >= 240:
            self.messagebox.showerror(APP_NAME, "路径层级过深，模型内部文件可能超过 Windows 默认长度限制。\n"
                                      "请选择更浅的工作目录，如 D:\\AI工坊")
            return
        cloud_roots = [Path(os.environ[key]) for key in ("OneDrive", "OneDriveCommercial", "OneDriveConsumer")
                       if os.environ.get(key)]
        if any(root == cloud or cloud in root.parents for cloud in cloud_roots):
            self.messagebox.showwarning(APP_NAME, "当前目录属于 OneDrive 同步区。模型可能被云端占位或同步锁定，"
                                        "建议改用普通本地目录。若继续，请确保始终保留离线副本。")
        new_lock = None
        try:
            test = root / (".studio_write_check_" + secrets.token_hex(8))
            test.write_bytes(b"OK")
            test.unlink()
            new_lock = WorkspaceLock(root)
            configure_environment(root)
            if recover_runtime_transaction(root):
                self.log("已恢复上次中断部署前的独立运行环境")
        except Exception as error:
            if new_lock:
                new_lock.close()
            self.messagebox.showerror(APP_NAME, "此目录不可写，请换一个目录：\n" + str(error))
            return
        if self.workspace_lock is not None:
            self.workspace_lock.close()
        self.workspace_lock = new_lock
        self.root_path = root
        self.pending_start_request = None
        self.last_output = None
        self.deployment_retry = 0
        self.ready = False
        self.basic_ready = False
        self.capabilities = {}
        self.result_card.pack_forget()
        self.preview_file = None
        self.preview_photo = None
        self.preview_caption.configure(text="分镜完成后，画面会逐幕出现在这里")
        self.draw_preview()
        self.folder_label.configure(text="工作目录  ·  " + str(root))
        self.update_setup()

    def log(self, message):
        message = str(message).strip()
        if not message:
            return
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.events.put(("log", timestamp + "  " + message[:1100]))
        if self.root_path:
            try:
                with self.log_lock:
                    file = self.root_path / ".studio" / "logs" / "studio.log"
                    if file.exists() and file.stat().st_size > 7 * 1024 * 1024:
                        rotated = file.with_suffix(".previous.log")
                        if rotated.exists():
                            rotated.unlink()
                        file.rename(rotated)
                    with file.open("a", encoding="utf-8") as handle:
                        handle.write("[%s] %s\n" % (datetime.datetime.now().isoformat(), message))
            except OSError:
                pass

    def set_status(self, message, progress=None):
        self.events.put(("status", message, progress))
        self.log(message)

    def refresh_buttons(self):
        busy = self.task not in (None, "部署") or self.blackbox_active
        self.start_btn.configure(state="normal" if self.root_path and not busy and
                                 self.pending_start_request is None else "disabled")
        self.open_btn.configure(state="normal" if self.last_output and self.last_output.exists()
                                 else "disabled")
        self.black_btn.configure(state="normal" if self.root_path and not self.blackbox_active else "disabled")
        self.prompt_box.configure(state="normal" if not busy else "disabled")

    def update_capability_label(self):
        if not hasattr(self, "capability_label"):
            return
        flags = self.capabilities if isinstance(self.capabilities, dict) else {}
        pieces = [("基础分镜/配音/剪辑", flags.get("basic")),
                  ("AI生图", flags.get("image_generation")),
                  ("语义与语音审核", flags.get("semantic_review") and flags.get("speech_review")),
                  ("原生动态视频", flags.get("native_video"))]
        label = "  ·  ".join(("✓ " if ok else "○ ") + text for text, ok in pieces)
        self.capability_label.configure(text=label, fg=self.palette["soft"])


    def update_setup(self):
        if not self.root_path or self.task or self.blackbox_active or self.setup_active:
            return
        self.capabilities = capability_report(self.root_path)
        self.ready = self.capabilities["full_offline"]
        self.basic_ready = self.capabilities["basic"]
        last_scan = read_json(self.root_path / ".studio" / "integrity_scan.json", {}).get("at")
        try:
            due_scan = (datetime.datetime.now() - datetime.datetime.fromisoformat(last_scan)).days >= 7
        except (ValueError, TypeError):
            due_scan = True
        self.force_integrity_scan = bool(self.ready and due_scan)
        self.update_capability_label()
        self.ready_badge.configure(text=("● 完全离线就绪" if self.ready else
                                         "● 基础离线就绪 · 有画面素材即可创作" if self.basic_ready else
                                         "● 正在准备离线创作环境"),
                                    fg=self.palette["green"] if self.ready or self.basic_ready else self.palette["amber"])
        self.install_stop.clear()
        self.task = "部署"
        self.setup_progress["value"] = 0
        self.set_status("正在后台检查本地创作环境", 1)
        self.refresh_buttons()
        self.setup_active = True
        self.setup_thread = threading.Thread(target=self.setup_worker, daemon=True)
        self.setup_thread.start()

    def verify_packages(self, tier, needs_piper=False):
        result = run_external([str(runtime_python(self.root_path)), str(Path(__file__).resolve()),
                               "--verify-packages", str(self.root_path), tier,
                               "piper" if needs_piper else "system"], self.root_path,
                              timeout=240, cancel=self.install_stop,
                              env=shell_env(self.root_path, offline=True), capture=True)
        for line in reversed(result.splitlines()):
            try:
                value = json.loads(line)
                if value.get("ok") and value.get("tier") == tier and all(
                        name in value.get("imports", {}) for name in required_imports(tier, needs_piper)):
                    return value
            except (ValueError, TypeError, AttributeError):
                continue
        raise RuntimeError("实际导入的组件不完整，不能跳过安装")

    def install_dependencies(self, needs_piper=False, tier="basic"):
        root = self.root_path
        active = root / ".studio" / "venv"
        backup = root / ".studio" / RUNTIME_BACKUP_FOLDER
        if backup.exists():
            recover_runtime_transaction(root)
        if packages_healthy(root, tier, needs_piper):
            try:
                self.verify_packages(tier, needs_piper)
                return
            except InterruptedError:
                raise
            except Exception as error:
                self.log("独立运行库需要重新部署：" + str(error)[:230])
        budget = installation_disk_budget(root, tier, needs_piper, replacement=True)
        if budget["free"] < budget["required"]:
            raise RuntimeError("安装空间不足：本阶段预计需要 %.1f GB，可用 %.1f GB。请换更大的工作目录或先导入离线资源包" % (
                budget["required"] / GB, budget["free"] / GB))
        old_manifest = root / ".studio" / "packages_ready.json"
        original_marker = old_manifest.read_bytes() if old_manifest.is_file() else None
        preserved = active.is_dir()
        if preserved:
            os.replace(active, backup)
            self.log("旧运行环境已备份到工作目录，候选环境验收前不会被删除")
        try:
            self._install_dependencies_in_place(needs_piper, tier)
            if not runtime_matches_host(root) or not packages_healthy(root, tier, needs_piper):
                raise RuntimeError("新环境的 Python 版本或依赖完整性不合格")
            self.verify_packages(tier, needs_piper)
        except BaseException:
            if preserved:
                if active.exists():
                    shutil.rmtree(active)
                os.replace(backup, active)
                if original_marker is not None:
                    old_manifest.write_bytes(original_marker)
                else:
                    old_manifest.unlink(missing_ok=True)
                self.log("已回滚到原有运行环境，避免安装失败损坏已有能力")
            else:
                if active.exists():
                    shutil.rmtree(active)
                old_manifest.unlink(missing_ok=True)
            raise
        else:
            if backup.exists():
                shutil.rmtree(backup)

    def _install_dependencies_in_place(self, needs_piper=False, tier="basic"):
        root = self.root_path
        python = runtime_python(root)
        site = runtime_site(root)
        marker = root / ".studio" / "packages_ready.json"
        prior = read_json(marker, {})
        unhealthy = False
        if packages_healthy(root, tier, needs_piper):
            try:
                self.verify_packages(tier, needs_piper)
                self.log("%s组件已通过真实导入检查，复用已有离线环境" %
                         ("基础" if tier == "basic" else "扩展"))
                return
            except InterruptedError:
                raise
            except Exception as error:
                unhealthy = True
                self.log("发现运行库损坏或依赖冲突，将自动修复：" + str(error)[:260])
        if not python.is_file():
            self.set_status("创建工作目录内的独立 Python 环境", 4)
            run_external([sys.executable, "-m", "venv", str(root / ".studio" / "venv")], root,
                         log=self.log, cancel=self.install_stop, timeout=180, capture=True)
        if not python.is_file():
            raise RuntimeError("无法创建独立 Python 环境，请检查 Python 是否包含 venv 组件")
        try:
            run_external([str(python), "-m", "pip", "--version"], root, timeout=35,
                         cancel=self.install_stop, capture=True)
        except InterruptedError:
            raise
        except Exception:
            run_external([str(python), "-m", "ensurepip", "--upgrade"], root, timeout=120,
                         cancel=self.install_stop, capture=True)
        offline_wheels = root / ".studio" / "offline_wheels"
        local_wheels = offline_wheels.is_dir() and any(offline_wheels.glob("*.whl"))
        source_options = ("https://pypi.tuna.tsinghua.edu.cn/simple", "https://pypi.org/simple")
        timings = {}
        workers = []
        if not local_wheels:
            self.set_status("检测可用的依赖安装线路", 5)
            def probe(item):
                timings[item] = probe_url(item + "/pillow/", 4)
            for item in source_options:
                thread = threading.Thread(target=probe, args=(item,), daemon=True)
                thread.start()
                workers.append(thread)
            for thread in workers:
                thread.join(5)
        indexes = sorted(source_options, key=lambda address: timings.get(address, float("inf")))
        base = [str(python), "-m", "pip", "install", "--disable-pip-version-check", "--no-input",
                "--prefer-binary", "--only-binary=:all:"]
        env = shell_env(root)
        env["PIP_DEFAULT_TIMEOUT"] = "35"
        env["PIP_RETRIES"] = "2"
        detected_gpu = gpu_info()
        torch_ok = (site / "torch").is_dir() and bool(list(site.glob("torch-*.dist-info")))
        if torch_ok:
            try:
                run_external([str(python), "-c", "import torch; "
                              "assert torch.__version__.split('+')[0]=='" + TORCH_VERSION + "'; "
                              "print(torch.__version__, torch.zeros(1).item())"], root,
                             timeout=120, cancel=self.install_stop,
                             env=shell_env(root, offline=True), capture=True)
            except InterruptedError:
                raise
            except Exception as error:
                torch_ok = False
                self.log("原有 PyTorch 不可用，准备修复：" + str(error)[:300])
        if not torch_ok:
            torch_error = None
            torch_sources = ([ ("本地安装包", str(offline_wheels), False) ] if local_wheels else [])
            torch_sources += torch_install_sources(detected_gpu, indexes)
            for label, source, wants_cuda in torch_sources:
                try:
                    self.set_status("安装 AI 计算引擎 · " + label, 10)
                    extra = ["--force-reinstall"] if (site / "torch").exists() else []
                    source_args = (["--no-index", "--find-links", source] if label == "本地安装包"
                                   else ["--index-url", source])
                    run_external(base + extra + source_args + ["torch==" + TORCH_VERSION], root,
                                 log=self.log, cancel=self.install_stop, timeout=2600, env=env, capture=True)
                    script = ("import torch; assert torch.__version__.split('+')[0]=='" + TORCH_VERSION + "'; "
                              "device='cuda' if " + str(wants_cuda) + " else 'cpu'; "
                              "x=torch.ones(2,device=device); print(device, float(x.sum().item()))")
                    run_external([str(python), "-c", script], root, timeout=150,
                                 cancel=self.install_stop, env=shell_env(root, offline=True), capture=True)
                    torch_error = None
                    break
                except InterruptedError:
                    raise
                except Exception as error:
                    torch_error = error
                    self.log("计算引擎安装失败，尝试其它线路：" + str(error)[:320])
            if torch_error:
                raise RuntimeError("计算引擎无法安装：" + str(torch_error))
        packages = list(CORE_PACKAGE_SPECS)
        if tier == "full":
            packages += list(EXTENDED_PACKAGE_SPECS)
        if needs_piper:
            packages += list(VOICE_PACKAGES)
        sources = ([ ("本地依赖包", ["--no-index", "--find-links", str(offline_wheels)]) ]
                   if local_wheels else [])
        sources += [(index, ["--index-url", index]) for index in indexes]
        last_error = None
        used_source = None
        for label, source_args in sources:
            try:
                self.set_status("安装%s离线组件 · %s" % ("基础" if tier == "basic" else "扩展", label), 12)
                self.log("依赖源：" + label)
                if unhealthy:
                    run_external(base + ["--force-reinstall", "--no-deps"] + source_args + packages,
                                 root, log=self.log, cancel=self.install_stop,
                                 timeout=3600, env=env, capture=True)
                run_external(base + source_args + packages, root, log=self.log,
                             cancel=self.install_stop, timeout=3600, env=env, capture=True)
                self.verify_packages(tier, needs_piper)
                run_external([str(python), "-m", "pip", "check"], root, timeout=120,
                             cancel=self.install_stop, env=shell_env(root, offline=True), capture=True)
                last_error = None
                used_source = label
                break
            except InterruptedError:
                raise
            except Exception as error:
                last_error = error
                self.log("该线路安装或导入校验失败，尝试其它线路：" + str(error)[:420])
        if last_error:
            raise RuntimeError("离线组件安装或依赖检查失败：" + str(last_error))
        if tier == "full" and not optional_ocr_ready(root):
            ocr_installed = False
            for label, source_args in sources:
                try:
                    self.set_status("尝试安装可选扫描件 OCR · " + label, 14)
                    run_external(base + source_args + list(OPTIONAL_OCR_PACKAGE_SPECS) +
                                 ["numpy>=1.26,<2.3"], root, log=self.log, cancel=self.install_stop,
                                 timeout=1300, env=env, capture=True)
                    output = run_external([str(python), str(Path(__file__).resolve()),
                                           "--verify-packages", str(root), "ocr", "system"],
                                          root, cancel=self.install_stop, timeout=180,
                                          env=shell_env(root, offline=True), capture=True)
                    if not any('"tier": "ocr"' in line and '"ok": true' in line.lower()
                               for line in output.splitlines()):
                        raise RuntimeError("OCR 功能实际导入检查没有通过")
                    run_external([str(python), "-m", "pip", "check"], root, cancel=self.install_stop,
                                 timeout=120, env=shell_env(root, offline=True), capture=True)
                    versions = installed_package_versions(root)
                    atomic_json(root / ".studio" / "ocr_ready.json",
                                {"runtime_version": RUNTIME_VERSION,
                                 "python": list(sys.version_info[:2]),
                                 "versions": {name: versions.get(name) for name in OPTIONAL_OCR_PACKAGE_IMPORTS},
                                 "completed": now_stamp(), "source": label})
                    ocr_installed = True
                    break
                except InterruptedError:
                    raise
                except Exception as error:
                    self.log("扫描件 OCR 属于可选能力，此安装线路未成功：" + str(error)[:260])
            if not ocr_installed:
                (root / ".studio" / "ocr_ready.json").unlink(missing_ok=True)
                self.log("扫描件 OCR 未准备好：文字 PDF、图像生成和视频剪辑不受影响")
            self.verify_packages(tier, needs_piper)
        previously_valid = prior.get("runtime_version") == RUNTIME_VERSION
        tiers = dict(prior.get("tiers", {})) if previously_valid else {}
        tiers[tier] = True
        if tier == "full":
            tiers["basic"] = True
        signatures = package_sentinels(root, tier, needs_piper)
        if not signatures:
            raise RuntimeError("组件安装后缺少关键模块，无法记录完整性标记")
        locked = installed_package_versions(root)
        pinned = {name: locked.get(name) for name in required_imports(tier, needs_piper)}
        if any(not value for value in pinned.values()):
            raise RuntimeError("组件安装后版本信息缺失")
        atomic_json(marker, {"runtime_version": RUNTIME_VERSION, "python": list(sys.version_info[:2]),
                             "time": now_stamp(), "source": used_source, "piper": needs_piper,
                             "tiers": tiers, "versions": locked, "sentinels": signatures})

    def prepare_native_automatically(self):
        root = self.root_path
        if native_video_model(root) or self.native_stop.is_set() or self.task == "创作":
            return
        gpu = gpu_info()
        power = system_power_state()
        available_memory = memory_info().get("available", 0)
        if (gpu.get("total_mb", 0) < NATIVE_AUTO_MIN_TOTAL_MB or
                gpu.get("free_mb", 0) < NATIVE_VIDEO_MIN_FREE_MB or
                available_memory < NATIVE_AUTO_MIN_RAM or power.get("on_battery")):
            self.log("优先保障轻量离线创作，当前不下载大型原生视频模型")
            return
        record_file = root / ".studio" / "native_auto.json"
        previous = read_json(record_file, {})
        try:
            last = datetime.datetime.fromisoformat(previous.get("checked", ""))
            recently_attempted = (datetime.datetime.now() - last).total_seconds() < NATIVE_AUTO_RETRY_SECONDS
        except (ValueError, TypeError):
            recently_attempted = False
        if recently_attempted and previous.get("status") in {
                "download_failed", "insufficient_disk", "network_unavailable", "resource_paused"}:
            self.log("大型视频模型沿用最近的环境检测结果，避免反复占用网络")
            return
        if shutil.disk_usage(root).free < NATIVE_AUTO_DISK_RESERVE + 20 * GB:
            atomic_json(record_file, {"checked": datetime.datetime.now().isoformat(),
                                      "status": "insufficient_disk"})
            self.log("磁盘空间不足以安全下载大型原生模型；离线图片运镜不受影响")
            return
        endpoints = choose_endpoints()
        accessible = [item for item in endpoints if math.isfinite(
            probe_url(item + "/api/models/" + NATIVE_AUTO_REPO, timeout=3))]
        if not accessible:
            atomic_json(record_file, {"checked": datetime.datetime.now().isoformat(),
                                      "status": "network_unavailable"})
            self.log("未检测到可用的大模型下载线路，跳过可选下载并保留离线创作能力")
            return
        self.log("高性能设备已识别，后台准备原生 AI 动态视频模型")
        errors = []
        for endpoint in accessible:
            if self.native_stop.is_set() or self.task == "创作":
                raise InterruptedError("已暂停大型模型的可选部署")
            current_power = system_power_state()
            ram = memory_info().get("available", 0)
            disk = shutil.disk_usage(root).free
            if current_power.get("on_battery") or ram < NATIVE_AUTO_MIN_RAM or disk < NATIVE_AUTO_DISK_RESERVE + MIN_INSTALL_FREE:
                atomic_json(record_file, {"checked": datetime.datetime.now().isoformat(),
                                          "status": "resource_paused"})
                self.log("检测到电池供电或系统资源不足，主动暂停可选大型模型下载")
                return
            try:
                run_external([str(runtime_python(root)), str(Path(__file__).resolve()),
                              "--fetch-native", str(root), endpoint], root, log=self.log,
                             cancel=self.native_stop, timeout=7200,
                             env=shell_env(root, endpoint=endpoint))
                if native_video_model(root):
                    atomic_json(record_file, {"checked": datetime.datetime.now().isoformat(),
                                              "status": "downloaded", "source": endpoint})
                    return
            except InterruptedError:
                raise
            except Exception as error:
                errors.append(str(error)[:220])
                self.log("原生模型下载线路不可用，尝试其它线路：" + errors[-1])
        atomic_json(record_file, {"checked": datetime.datetime.now().isoformat(),
                                  "status": "download_failed", "error_types": [
                                      diagnostic_exception_summary(item)["exception_type"] for item in errors]})
        self.log("大型视频下载未成功，默认继续使用完全离线的图片运镜")

    def validate_optional_native(self):
        root = self.root_path
        if not native_video_model(root) or native_inference_ready(root):
            return
        if self.native_stop.is_set() or self.task == "创作":
            return
        marker = read_json(root / ".studio" / "native_ready.json", {})
        if native_load_ready(root) and marker.get("smoke_status") == REVIEW_UNAVAILABLE:
            try:
                checked = datetime.datetime.fromisoformat(marker.get("checked", ""))
                if (datetime.datetime.now() - checked).total_seconds() < NATIVE_AUTO_RETRY_SECONDS:
                    self.log("原生模型实际推理未通过，稍后再进行资源验证；当前继续使用图片运镜")
                    return
            except (TypeError, ValueError):
                pass
        gpu = gpu_info()
        if gpu.get("free_mb", 0) < NATIVE_VIDEO_MIN_FREE_MB:
            self.log("原生模型已下载但当前空闲显存不足，继续使用图片动态运镜")
            return
        try:
            result = run_external([str(runtime_python(root)), str(Path(__file__).resolve()),
                                   "--check-native", str(root)], root, log=self.log,
                                  cancel=self.native_stop, timeout=NATIVE_SMOKE_TIMEOUT,
                                  env=shell_env(root, offline=True), capture=True)
            if not native_inference_ready(root) or '"inference_tested": true' not in result.lower():
                raise RuntimeError("原生视频真实推理与解码验收不完整")
            self.log("原生视频模型已通过实际推理、编码与离线解码验收")
        except InterruptedError:
            raise
        except (RuntimeError, OSError, MemoryError, TimeoutError) as error:
            self.log("原生视频可选验收未通过，已自动保留图片运镜：" + str(error)[:160])

    def start_native_background(self):
        if (not self.root_path or self.task is not None or self.setup_active or
                self.pending_start_request is not None or not self.capabilities.get("full_offline")):
            return
        if self.native_auto_thread is not None and self.native_auto_thread.is_alive():
            return
        if system_power_state().get("on_battery"):
            return
        self.native_stop.clear()
        self.native_auto_thread = threading.Thread(target=self.native_background_worker, daemon=True)
        self.native_auto_thread.start()

    def native_background_worker(self):
        finished = threading.Event()
        def monitor():
            busy_streak = 0
            last_cpu = None
            while not finished.wait(RESOURCE_MONITOR_INTERVAL):
                try:
                    if self.native_stop.is_set() or self.task == "创作":
                        self.native_stop.set()
                        return
                    if (system_power_state().get("on_battery") or
                            memory_info().get("available", 0) < NATIVE_AUTO_MIN_RAM or
                            shutil.disk_usage(self.root_path).free < NATIVE_AUTO_DISK_RESERVE + MIN_INSTALL_FREE):
                        self.log("可选模型下载已让出电量、内存或磁盘资源")
                        self.native_stop.set()
                        return
                    current_cpu = cpu_time_sample()
                    if current_cpu and last_cpu:
                        total = current_cpu[1] - last_cpu[1]
                        if total > 0:
                            busy = 1 - (current_cpu[0] - last_cpu[0]) / total
                            busy_streak = busy_streak + 1 if busy > RESOURCE_MONITOR_CPU_LIMIT else 0
                    last_cpu = current_cpu
                    if busy_streak >= RESOURCE_PRESSURE_STREAK + 1:
                        self.log("设备持续繁忙，自动暂停可选模型下载以保障其它软件")
                        self.native_stop.set()
                        return
                except (OSError, ValueError):
                    continue
        watcher = threading.Thread(target=monitor, daemon=True)
        watcher.start()
        try:
            self.prepare_native_automatically()
            if not self.native_stop.is_set():
                self.validate_optional_native()
            self.events.put(("native_done", True))
        except InterruptedError:
            self.events.put(("native_done", False))
        except Exception as error:
            self.log("可选原生模型初始化未完成：" + str(error)[:200])
            self.events.put(("native_done", False))
        finally:
            finished.set()
            watcher.join(timeout=1.0)

    def setup_worker(self):
        root = self.root_path
        deep = self.force_integrity_scan
        self.force_integrity_scan = False
        try:
            if deep:
                self.set_status("正在逐一检查模型文件完整 SHA-256", 2)
            if not deep and is_ready(root):
                diagnostics = read_json(root / ".studio" / "ready.json", {}).get("diagnostic", {})
                if not voice_backend_operational(root, diagnostics.get("voice_backend"), force=True):
                    self.log("系统中文语音发生变化，准备修复基础离线配音环境")
                else:
                    self.events.put(("setup_done", True,
                                     "离线创作已就绪；原生视频按本机资源自动选择"))
                    return
            needs_basic = not basic_ready(root)
            needs_voice = not test_system_chinese_voice(root)
            budget = installation_disk_budget(root, "basic" if needs_basic else "full", needs_voice,
                                              replacement=needs_basic)
            self.log("动态部署预算：预计 %.2f GB，可用 %.2f GB，未安装模型 %s" % (
                budget["required"] / GB, budget["free"] / GB,
                ",".join(budget["missing_models"]) or "无"))
            if budget["free"] < budget["required"]:
                raise RuntimeError("工作目录空间不足：当前阶段预计还需 %.1f GB（含下载缓存、运行库和安全余量），可用 %.1f GB" % (
                    budget["required"] / GB, budget["free"] / GB))
            if (not basic_ready(root) or deep and (
                    not model_download_complete(root, MODEL_SPECS[0], deep=True) or
                    not voice_backend_operational(root, "sapi", force=True) and
                    not voice_download_complete(root, deep=True)) or
                    not voice_backend_operational(root,
                        read_json(root / ".studio" / "basic_ready.json", {}).get(
                            "diagnostic", {}).get("voice_backend"))):
                self.set_status("检查离线中文语音与系统能力", 3)
                needs_piper = not test_system_chinese_voice(root)
                self.install_dependencies(needs_piper=needs_piper, tier="basic")
                if self.install_stop.is_set():
                    raise InterruptedError("部署已停止")
                missing_director = not model_download_complete(root, MODEL_SPECS[0], deep=deep)
                missing_voice = needs_piper and not voice_download_complete(root, deep=deep)
                endpoints = choose_endpoints() if missing_director or missing_voice else []
                if missing_director:
                    self.set_status("优先安装本地分镜导演", 18)
                    self.fetch_model_with_fallback(0, MODEL_SPECS[0], endpoints, deep=deep)
                if missing_voice:
                    self.set_status("准备中文离线配音", 34)
                    errors = []
                    for endpoint in endpoints:
                        try:
                            run_external([str(runtime_python(root)), str(Path(__file__).resolve()),
                                          "--fetch-voice", str(root), endpoint], root,
                                         log=self.log, cancel=self.install_stop, timeout=1800,
                                         env=shell_env(root, endpoint=endpoint), capture=False)
                            if voice_download_complete(root):
                                break
                        except InterruptedError:
                            raise
                        except Exception as error:
                            errors.append(str(error))
                    if not voice_download_complete(root):
                        raise RuntimeError("中文语音模型下载失败：" + " / ".join(errors)[-450:])
                self.set_status("验收基础离线创作能力", 44)
                diagnostics = self.verify_runtime("basic")
                atomic_json(root / ".studio" / "basic_ready.json",
                            {"runtime_version": RUNTIME_VERSION, "completed": now_stamp(),
                             "python": list(sys.version_info[:2]), "diagnostic": diagnostics})
            self.events.put(("setup_basic", True, "基础离线创作已就绪，正在补齐图像生成、语义审校和语音识别"))
            if self.install_stop.is_set():
                raise InterruptedError("部署已暂停")
            self.install_dependencies(needs_piper=not test_system_chinese_voice(root), tier="full")
            missing = [(index, spec) for index, spec in enumerate(MODEL_SPECS[1:], 1)
                       if not model_download_complete(root, spec, deep=deep)]
            if missing:
                endpoints = choose_endpoints()
                self.log("模型线路探测仅用于排序；即使 HEAD/GET 探测失败也直接尝试实际下载")
                parallel = (min(MAX_DOWNLOAD_PROCESSES, len(missing)) if
                            shutil.disk_usage(root).free >= MIN_PARALLEL_DOWNLOAD_FREE and
                            available_threads() >= 3 else 1)
                self.set_status("补齐 %d 项扩展离线模型" % len(missing), 48)
                done = 0
                finished = threading.Event()
                def monitor():
                    while not finished.wait(6):
                        try:
                            total = 0
                            for _, spec in missing:
                                folder = model_path(root, spec[2])
                                staging = folder.with_name(folder.name + ".downloading")
                                target = staging if staging.exists() else folder
                                total += sum(file.stat().st_size for file in target.rglob("*") if file.is_file())
                            self.set_status("扩展模型 %d/%d · 已保存 %.2f GB" % (done, len(missing), total / GB),
                                            48 + int(37 * done / len(missing)))
                        except OSError:
                            pass
                threading.Thread(target=monitor, daemon=True).start()
                try:
                    with concurrent.futures.ThreadPoolExecutor(max_workers=parallel) as executor:
                        futures = [executor.submit(self.fetch_model_with_fallback, index, spec, endpoints, deep)
                                   for index, spec in missing]
                        try:
                            for future in concurrent.futures.as_completed(futures):
                                future.result()
                                done += 1
                                self.set_status("扩展离线模型 %d/%d 已就绪" % (done, len(missing)),
                                                48 + int(37 * done / len(missing)))
                        except BaseException:
                            self.install_stop.set()
                            for future in futures:
                                future.cancel()
                            raise
                finally:
                    finished.set()
            if self.install_stop.is_set():
                raise InterruptedError("部署已停止")
            self.set_status("执行完整离线模型与视频编码验收", 92)
            diagnostics = self.verify_runtime("full")
            atomic_json(root / ".studio" / "ready.json",
                        {"version": APP_VERSION, "runtime_version": RUNTIME_VERSION,
                         "completed": datetime.datetime.now().isoformat(),
                         "python": list(sys.version_info[:2]), "smoke_test": True,
                         "model_signature": model_signature(root), "diagnostic": diagnostics})
            if deep:
                atomic_json(root / ".studio" / "integrity_scan.json", {
                    "at": datetime.datetime.now().isoformat(), "status": "full_model_hashes_verified"})
            self.events.put(("setup_done", True,
                             "完整离线能力已验收；动态视频生成方式已自动选择"))
        except InterruptedError:
            self.events.put(("setup_done", False, "扩展部署已暂停，下载进度保留"))
        except Exception:
            self.log(traceback.format_exc())
            explanation = traceback.format_exc().splitlines()[-1][:350]
            self.events.put(("setup_done", False, "扩展部署未完成：" + explanation + "。可重试继续"))
        finally:
            self.setup_active = False

    def fetch_model_with_fallback(self, index, spec, endpoints, deep=False):
        if model_download_complete(self.root_path, spec, deep=deep):
            return
        errors = []
        for endpoint in endpoints:
            if self.install_stop.is_set():
                raise InterruptedError("部署已停止")
            try:
                run_external([str(runtime_python(self.root_path)), str(Path(__file__).resolve()),
                              "--fetch-model", str(self.root_path), str(index), endpoint] +
                             (["deep"] if deep else []),
                             self.root_path, log=self.log, cancel=self.install_stop,
                             timeout=4000, env=shell_env(self.root_path, endpoint=endpoint))
                if model_download_complete(self.root_path, spec, deep=deep):
                    return
                raise RuntimeError("模型文件完整性校验失败")
            except InterruptedError:
                raise
            except Exception as error:
                errors.append(str(error)[:260])
                self.log("%s线路失败：%s" % (spec[0], str(error)[:220]))
        raise RuntimeError("模型 %s 未下载成功，可联网重试：%s" % (spec[0], " | ".join(errors)[-550:]))

    def verify_runtime(self, tier):
        root = self.root_path
        result = run_external([str(runtime_python(root)), str(Path(__file__).resolve()),
                               "--check-runtime", str(root), tier], root, log=self.log,
                              cancel=self.install_stop, timeout=900,
                              env=shell_env(root, offline=True), capture=True)
        required = {"director", "encoder", "voice"} if tier == "basic" else {
            "director", "encoder", "voice", "listener", "inspector", "painter"}
        for line in reversed(result.splitlines()):
            try:
                value = json.loads(line)
                if (value.get("ok") and value.get("tier") == tier
                        and all(value.get("smoke_test", {}).get(item) == "passed" for item in required)
                        and value.get("voice_backend") in {"sapi", "piper"}):
                    return value
            except (ValueError, TypeError, AttributeError):
                continue
        raise RuntimeError("实际离线推理验收不完整（%s），不能宣称完全就绪" % tier)

    def resume_setup(self):
        if not self.root_path or self.task or is_ready(self.root_path):
            return
        if self.setup_active:
            self.root.after(600, self.resume_setup)
        else:
            self.update_setup()

    def capture_request(self):
        prompt = self.prompt_box.get("1.0", "end-1c").strip()
        if prompt.startswith("例："):
            prompt = ""
        return {"prompt": prompt, "files": {k: list(v) for k, v in self.assets.items()},
                "duration": int(self.duration.get()), "quality": self.quality.get(), "aspect": self.aspect.get(),
                "audio_role": self.audio_role.get(), "source_audio_role": self.source_audio_role.get(),
                "visual_mode": self.visual_mode.get()}

    def can_pause_optional_install(self, request):
        files = request.get("files", {}) if isinstance(request, dict) else {}
        has_visual = any(files.get(role) for role in ("图片", "首帧", "尾帧", "视频"))
        if not has_visual:
            return bool(capability_report(self.root_path, request)["create_allowed"])
        if self.basic_ready or (self.root_path / ".studio" / "basic_ready.json").is_file():
            return True
        return bool(capability_report(self.root_path, request)["create_allowed"])

    def start_job(self):
        if not self.root_path or self.task not in (None, "部署") or self.blackbox_active:
            return
        request = self.capture_request()
        if not request["prompt"]:
            self.messagebox.showinfo(APP_NAME, "请输入想制作的视频内容")
            self.prompt_box.focus_set()
            return
        absent = [name for paths in request["files"].values() for name in paths if not Path(name).is_file()]
        if absent:
            self.messagebox.showerror(APP_NAME, "以下素材已不可用：\n" + "\n".join(absent[:4]))
            return
        self.capabilities = capability_report(self.root_path, request)
        self.native_stop.set()
        if self.task == "部署" or self.setup_active:
            self.pending_start_request = request
            if self.can_pause_optional_install(request):
                self.install_stop.set()
                self.set_status("已有能力可完成本次创作，正在暂停扩展安装并释放资源")
            else:
                self.set_status("已接收创作需求，继续准备所需离线模型；基础可用时优先启动")
            self.refresh_buttons()
            self.root.after(220, self.launch_queued_job)
            return
        if not self.capabilities["create_allowed"]:
            self.pending_start_request = request
            self.set_status("已接收创作需求，所需模型尚未全部就绪；部署完成后自动启动")
            self.refresh_buttons()
            self.update_setup()
            return
        if self.native_auto_thread is not None and self.native_auto_thread.is_alive():
            self.pending_start_request = request
            self.refresh_buttons()
            self.root.after(220, self.launch_queued_job)
            return
        self.launch_job(request)

    def launch_queued_job(self):
        if self.pending_start_request is None:
            return
        if (self.setup_active or (self.setup_thread and self.setup_thread.is_alive()) or
                (self.native_auto_thread and self.native_auto_thread.is_alive())):
            self.native_stop.set()
            if self.can_pause_optional_install(self.pending_start_request):
                self.install_stop.set()
            self.root.after(220, self.launch_queued_job)
            return
        if self.task is not None:
            self.root.after(220, self.launch_queued_job)
            return
        request = self.pending_start_request
        self.capabilities = capability_report(self.root_path, request)
        if not self.capabilities["create_allowed"]:
            self.set_status("所需模型尚未验收：提供画面素材可使用基础离线剪辑，否则需等待完整部署")
            return
        self.pending_start_request = None
        self.launch_job(request)

    def launch_job(self, request):
        try:
            self.capabilities = require_request_capabilities(self.root_path, request)
        except (RuntimeError, OSError) as error:
            self.set_status("任务启动前能力检查失败：" + str(error)[:230])
            self.refresh_buttons()
            return
        if self.task is not None or self.setup_active or (self.setup_thread and self.setup_thread.is_alive()):
            self.pending_start_request = request
            self.root.after(180, self.launch_queued_job)
            return
        self.task = "创作"
        self.stop_event.clear()
        self.last_output = None
        self.last_job = None
        self.preview_file = None
        self.preview_photo = None
        self.scene_entries = []
        self.scene_rows = []
        for item in self.scene_rows_frame.winfo_children():
            item.destroy()
        self.scene_count.configure(text="正在规划")
        self.scene_empty_label = self.label(self.scene_rows_frame, "AI 正在理解需求并编写镜头", 9,
                                             self.palette["muted"])
        self.scene_empty_label.pack(anchor="w")
        self.result_card.pack_forget()
        self.result_card.winfo_children()[0].configure(text="作品已完成", fg=self.palette["green"])
        self.creation_progress["value"] = 0
        self.progress_text.configure(text="0%")
        self.preview_caption.configure(text="正在准备创作任务")
        self.render_task_state("preparing")
        self.draw_preview()
        self.refresh_buttons()
        threading.Thread(target=self.job_worker, args=(request,), daemon=True).start()

    def job_worker(self, request):
        request_file = self.root_path / ".studio" / "tmp" / ("request_" + now_stamp() + ".json")
        stop_file = self.root_path / ".studio" / "tmp" / ("stop_" + now_stamp() + ".signal")
        self.job_stop_file = stop_file
        try:
            atomic_json(request_file, request)
            outcome = {}
            def receive(line):
                if line.startswith(PROGRESS_PREFIX):
                    try:
                        event = json.loads(line[len(PROGRESS_PREFIX):])
                        if event.get("type") == "status":
                            self.set_status(event["message"], event.get("progress"))
                        elif event.get("type") == "job_path":
                            self.last_job = Path(event["path"])
                        elif event.get("type") == "result":
                            outcome["output"] = event["output"]
                        elif event.get("type") in {"phase", "storyboard", "scene_active", "scene_ready", "scene_review", "reference_warning"}:
                            self.events.put(("project_event", event))
                    except (ValueError, KeyError, TypeError) as error:
                        self.log("进度事件无法读取：" + str(error))
                else:
                    self.log(line)
            run_external([str(runtime_python(self.root_path)), "-u", str(Path(__file__).resolve()), "--run-job",
                          str(self.root_path), str(request_file), str(stop_file)], self.root_path,
                         cancel=self.stop_event, timeout=21600, env=shell_env(self.root_path, offline=True),
                          capture=True, on_line=receive, stop_file=stop_file, stop_grace=STOP_GRACE_SECONDS)
            if not outcome.get("output"):
                raise RuntimeError("创作进程未返回完成的成品路径")
            self.events.put(("job_done", True, outcome["output"]))
        except InterruptedError:
            self.events.put(("job_done", False, "已停止，已完成的中间素材仍保存在工作目录"))
        except Exception:
            self.log(traceback.format_exc())
            self.events.put(("job_done", False, "生成失败：" + traceback.format_exc().splitlines()[-1][:260]))
        finally:
            request_file.unlink(missing_ok=True)
            stop_file.unlink(missing_ok=True)
            self.job_stop_file = None

    def open_output(self):
        if not self.last_output:
            return
        folder = self.last_output.parent
        try:
            if os.name == "nt":
                os.startfile(str(folder))
            else:
                subprocess.Popen(["xdg-open", str(folder)])
        except OSError as error:
            self.messagebox.showerror(APP_NAME, "打开文件夹失败：" + str(error))

    def blackbox(self):
        if not self.root_path or self.blackbox_active:
            return
        request = self.capture_request()
        self.blackbox_active = True
        self.refresh_buttons()
        def work():
            try:
                value = export_black_box(self.root_path, request, self.last_job, self.log,
                                         include_private=False)
                self.events.put(("black_done", True, str(value)))
            except Exception:
                self.log(traceback.format_exc())
                self.events.put(("black_done", False, traceback.format_exc().splitlines()[-1]))
        threading.Thread(target=work, daemon=True).start()

    def process_events(self):
        try:
            for _ in range(80):
                try:
                    event = self.events.get_nowait()
                except queue.Empty:
                    break
                category = event[0]
                if category == "log":
                    continue
                elif category == "status":
                    self.stage_label.configure(text=event[1][:250], fg=self.palette["soft"])
                    if event[2] is not None:
                        percent = max(0, min(100, int(event[2])))
                        if self.task == "创作":
                            self.creation_progress["value"] = percent
                            self.progress_text.configure(text="%d%%" % percent)
                        else:
                            self.setup_progress["value"] = percent
                elif category == "project_event":
                    data = event[1]
                    kind = data.get("type")
                    if kind == "reference_warning":
                        self.stage_label.configure(text=str(data.get("message", "部分参考内容未采用")),
                                                   fg=self.palette["amber"])
                        self.log("参考素材警示：" + str(data.get("message", "")))
                    elif kind == "phase":
                        self.render_task_state(str(data.get("phase", "idle")))
                    elif kind == "storyboard":
                        scenes = data.get("scenes", [])
                        if isinstance(scenes, list):
                            self.render_storyboard(str(data.get("title", "")), scenes)
                    elif kind in {"scene_active", "scene_ready", "scene_review"}:
                        index = data.get("index", -1)
                        if isinstance(index, int):
                            state = "active" if kind == "scene_active" else "reviewing" if kind == "scene_review" else "done"
                            self.render_scene_state(index, state, data.get("preview"),
                                                    str(data.get("review", "")))
                elif category == "setup_basic":
                    self.capabilities = capability_report(self.root_path)
                    self.update_capability_label()
                    self.ready = False
                    self.basic_ready = bool(event[1])
                    self.ready_badge.configure(text="● 基础离线就绪 · 可使用画面素材创作", fg=self.palette["green"])
                    self.stage_label.configure(text=event[2], fg=self.palette["soft"])
                    self.refresh_buttons()
                    if self.pending_start_request is not None and self.can_pause_optional_install(
                            self.pending_start_request):
                        self.install_stop.set()
                        self.root.after(220, self.launch_queued_job)
                elif category == "setup_done":
                    if self.task != "部署":
                        continue
                    self.task = None
                    self.capabilities = capability_report(self.root_path)
                    self.update_capability_label()
                    self.ready = self.capabilities["full_offline"]
                    self.basic_ready = self.capabilities["basic"]
                    self.ready_badge.configure(text=("● 完整离线就绪 · 原生视频已实测" if self.capabilities.get("native_video")
                                                     else "● 完整离线就绪 · 智能图片运镜") if self.ready else
                                               "● 基础离线就绪 · 用户素材可创作" if self.basic_ready else
                                               "● 正在准备离线环境",
                                               fg=self.palette["green"] if self.ready or self.basic_ready
                                               else self.palette["amber"])
                    message = (event[2] + "；基础配音与素材剪辑不受影响" if self.basic_ready and not self.ready
                               else event[2])
                    self.stage_label.configure(text=message[:250],
                                               fg=self.palette["green"] if event[1] or self.basic_ready
                                               else self.palette["danger"])
                    if self.capabilities["full_offline"]:
                        self.setup_progress["value"] = 100
                    self.refresh_buttons()
                    self.refresh_smart_suggestions()
                    if self.ready:
                        self.deployment_retry = 0
                    elif not any(term in str(event[2]) for term in
                                 ("空间不足", "内存不足", "不支持", "不兼容", "文件夹不可写", "权限不足")):
                        self.deployment_retry += 1
                        backoff = min(15 * 60 * 1000, 20 * 1000 * (2 ** min(5, self.deployment_retry - 1)))
                        self.root.after(backoff, self.update_setup)
                    if self.pending_start_request is not None:
                        self.root.after(180, self.launch_queued_job)
                    elif self.ready:
                        self.root.after(450, self.start_native_background)
                elif category == "job_done":
                    self.task = None
                    if event[1]:
                        self.last_output = Path(event[2])
                        self.creation_progress["value"] = 100
                        self.progress_text.configure(text="100%")
                        self.render_task_state("complete")
                        self.stage_label.configure(text="成片已交付 · " + str(event[2]),
                                                   fg=self.palette["green"])
                        self.show_result_panel(self.last_output)
                    else:
                        self.stage_label.configure(text=event[2], fg=self.palette["danger"])
                        self.show_job_error(event[2])
                    self.refresh_buttons()
                    if event[1] and self.root_path and shutil.disk_usage(self.root_path).free < MIN_INSTALL_FREE:
                        threading.Thread(target=cleanup_completed_cache,
                                         args=(self.root_path,), daemon=True).start()
                    self.root.after(450, self.resume_setup)
                    if event[1]:
                        self.root.after(800, self.start_native_background)
                elif category == "cache_done":
                    self.task = None
                    self.stage_label.configure(text=event[2],
                                               fg=self.palette["green"] if event[1] else self.palette["danger"])
                    self.refresh_buttons()
                elif category == "import_done":
                    self.task = None
                    self.stage_label.configure(text=event[2], fg=self.palette["green"] if event[1]
                                               else self.palette["danger"])
                    self.refresh_buttons()
                    if event[1]:
                        self.root.after(150, self.update_setup)
                elif category == "cleanup_done":
                    self.task = None
                    self.stage_label.configure(text=event[2], fg=self.palette["green"] if event[1]
                                               else self.palette["amber"])
                    self.refresh_buttons()
                elif category == "native_done":
                    self.capabilities = capability_report(self.root_path)
                    self.update_capability_label()
                    self.refresh_smart_suggestions()
                elif category == "black_done":
                    self.blackbox_active = False
                    self.refresh_buttons()
                    if event[1]:
                        self.messagebox.showinfo(APP_NAME, "黑匣子已保存：\n" + event[2]
                                                 + "\n\n分享前请确认压缩包内容。")
                    else:
                        self.messagebox.showerror(APP_NAME, "黑匣子导出失败：\n" + event[2])
        finally:
            try:
                self.root.after(120, self.process_events)
            except self.tk.TclError:
                pass

    def on_close(self):
        if self.task in {"部署", "创作"} or self.blackbox_active or (self.native_auto_thread and self.native_auto_thread.is_alive()):
            if not self.messagebox.askyesno(APP_NAME, "当前任务正在执行，确定退出？下次可续传已下载内容。"):
                return
            self.stop_event.set()
            self.install_stop.set()
            self.native_stop.set()
            if self.job_stop_file is not None:
                self.job_stop_file.touch()
            with RUNNING_CHILDREN_LOCK:
                children = list(RUNNING_CHILDREN)
            for proc in children:
                stop_process_tree(proc)
        if self.workspace_lock is not None:
            self.workspace_lock.close()
        self.root.destroy()

    def run(self):
        self.root.mainloop()



def main():
    args = sys.argv[1:]
    if (sys.version_info[:2] < MIN_PYTHON or sys.version_info[:2] > MAX_PYTHON
            or struct.calcsize("P") != 8):
        raise SystemExit("需要 Python 3.10–3.13 的 64 位解释器")
    if os.name != "nt":
        raise SystemExit("本程序仅支持 Windows 11 x64")
    if args and args[0] == "--fetch-native" and len(args) == 3:
        download_native_worker(args[1], args[2])
        return
    if args and args[0] == "--fetch-model" and len(args) in (4, 5):
        download_model_worker(args[1], int(args[2]), args[3],
                              deep=len(args) == 5 and args[4] == "deep")
        return
    if args and args[0] == "--render-native" and len(args) in (5, 6, 7, 8):
        native_video_worker(args[1], args[2], args[3], args[4],
                            float(args[5]) if len(args) >= 6 else 3.0,
                            (args[6] or None) if len(args) >= 7 else None,
                            args[7] if len(args) == 8 else "横屏 16:9")
        return
    if args and args[0] == "--verify-packages" and len(args) == 4:
        verify_packages_worker(args[1], args[2], args[3] == "piper")
        return
    if args and args[0] == "--check-native" and len(args) == 2:
        check_native_worker(args[1])
        return
    if args and args[0] == "--check-runtime" and len(args) in (2, 3):
        check_runtime_worker(args[1], args[2] if len(args) == 3 else "full")
        return
    if args and args[0] == "--fetch-voice" and len(args) == 3:
        download_voice_worker(args[1], args[2])
        return
    if args and args[0] == "--speak" and len(args) == 4:
        piper_speak_worker(args[1], args[2], args[3])
        return
    if args and args[0] == "--speak-server" and len(args) == 2:
        piper_server_worker(args[1])
        return
    if args and args[0] == "--read-document" and len(args) == 4:
        configure_environment(args[1])
        Path(args[3]).write_text(document_text(args[2]), encoding="utf-8")
        return
    if args and args[0] == "--run-job" and len(args) == 4:
        root = Path(args[1])
        configure_environment(root)
        os.environ.update({"HF_HUB_OFFLINE": "1", "TRANSFORMERS_OFFLINE": "1", "DIFFUSERS_OFFLINE": "1"})
        request = read_json(args[2], {})
        if not request.get("prompt"):
            raise RuntimeError("创作请求没有有效的提示词")
        def emit(payload):
            print(PROGRESS_PREFIX + json.dumps(payload, ensure_ascii=False), flush=True)
        def event(message, progress=None):
            emit({"type": "status", "message": message, "progress": progress})
        studio = StudioJob(root, request, event, StopSignal(args[3]),
                           lambda line: print(line, flush=True), emit=emit)
        print(PROGRESS_PREFIX + json.dumps({"type": "job_path", "path": str(studio.job)},
                                            ensure_ascii=False), flush=True)
        output = studio.start()
        print(PROGRESS_PREFIX + json.dumps({"type": "result", "output": str(output)},
                                            ensure_ascii=False), flush=True)
        return
    StudioUI().run()


if __name__ == "__main__":
    main()
