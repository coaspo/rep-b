import abc
import calendar
import datetime
import glob
import json
import logging
import os.path
import re
import traceback
from typing import Dict, List

log = logging.getLogger(__name__)


class InvalidOperation(Exception):
    pass


class JsonFileStorage:
    def __init__(self, save_dir: str, file_pfx: str, latest_file_name: str or None):
        self._active_file_index: int
        self._file_pfx: str = file_pfx
        self._files_paths: List[str]
        self._file_description: str
        self._latest_file_name: str = latest_file_name
        self._latest_file_number: int
        self._save_dir: str = save_dir
        self._initialize()

    def _initialize(self):
        self._save_dir, err_msg = JsonFileStorage._possibly_create_save_dir(self._save_dir)
        if err_msg is None:
            self._latest_file_number, self._active_file_index, self._files_paths = JsonFileStorage._get_file_paths(
                self._file_pfx,
                self._latest_file_name,
                self._save_dir)
        else:
            raise Exception('JsonFileStorage failed - ' + err_msg)

    @property
    def file_description(self):
        return self._file_description

    @property
    def file_path(self):
        return self._files_paths[self._active_file_index]

    @property
    def file_pfx(self):
        return self._file_pfx

    @property
    def is_file_list_empty(self):
        return len(self._files_paths) == 0

    @property
    def latest_file_name(self):
        return self._latest_file_name

    @property
    def save_dir(self):
        return self._save_dir

    def decrement_file_index(self):
        self._ensure_file_path_list_is_not_empty()
        if self._active_file_index != 0:
            self._active_file_index -= 1

    def file_info(self) -> str:
        file_path = self._files_paths[self._active_file_index]
        seconds_since_created = os.path.getmtime(file_path)
        create_ts = datetime.datetime.utcfromtimestamp(seconds_since_created).isoformat()[:22]
        # remove T in, for example, create_ts = 2019-12-11T19:20:48.85
        create_ts = create_ts[2:10] + ' ' + create_ts[11:16]
        day_index = datetime.datetime.utcfromtimestamp(seconds_since_created).weekday()
        count = str(self._active_file_index + 1) + '/' + str(len(self._files_paths))
        info = count + '  ' + os.path.basename(file_path) + '  ' + create_ts + ' ' + calendar.day_name[day_index][0:3]
        return info

    def increment_file_index(self):
        self._ensure_file_path_list_is_not_empty()
        if self._active_file_index != len(self._files_paths) - 1:
            self._active_file_index += 1

    def read_file(self) -> dict:
        file_path = self._files_paths[self._active_file_index]
        try:
            with open(file_path, "r", encoding='utf8') as f:
                data_dict = json.load(f)
        except OSError:
            # reinitialize to fix for example no files found error.
            self._initialize()
            file_path = self._files_paths[self._active_file_index]
            with open(file_path, "r", encoding='utf8') as f:
                data_dict = json.load(f)
        self._file_description = self.file_info()
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}\ndata_dict=\n{data_dict}')
        return data_dict

    def reset_file_prefix(self, file_pfx: str) -> None:
        self._file_pfx = file_pfx
        self._latest_file_number, self._active_file_index, self._files_paths = JsonFileStorage._get_file_paths(
            file_pfx,
            None,
            self._save_dir)

    def delete_file(self) -> str:
        if len(self._files_paths) == 1:
            raise Exception("Cannot delete last file.")
        file_path = self._files_paths[self._active_file_index]
        os.remove(file_path)
        self._files_paths.remove(file_path)
        self._active_file_index -= 1

    def save_new_file(self, data_dict: dict) -> str:
        file_num = self._latest_file_number + 1
        file_index = self._active_file_index + 1
        file_path = self._save_dir + '/' + self._file_pfx + '.' + str(file_num) + '.json'
        if file_index > len(self._files_paths):
            raise AttributeError(
                f'Index Error:  _file_path_index= {file_index}' +
                f'(len(_files_paths)={len(self._files_paths)}), ')
        with open(file_path, "w", encoding='utf8') as f:
            json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)
        self._files_paths.append(file_path)
        self._latest_file_number = file_num
        self._active_file_index = file_index
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={file_path}')
        self._file_description = self.file_info()
        return file_path

    def update_file(self, data_dict: dict):
        with open(self._files_paths[self._active_file_index], "w", encoding='utf8') as f:
            json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'file_path={self._files_paths[self._active_file_index]}')

    def _ensure_file_path_list_is_not_empty(self):
        if len(self._files_paths) == 0:
            raise AttributeError(f'No files, "{self._file_pfx}.<unique-num>.json" files in: {self._save_dir}')

    @staticmethod
    def _get_file_paths(file_pfx: str, latest_file_name: str or None, save_dir: str) -> (str, str):
        file_paths = glob.glob(save_dir + '/' + file_pfx + '*.json')
        if len(file_paths) == 0:
            return 0, -1, []
        file_paths.sort()
        file_nums = []
        filtered_file_paths = []
        file_index = len(file_paths) - 1
        for i, file_path in enumerate(file_paths):
            x = file_path.split('.')
            if len(x) > 0 and x[1].isnumeric():
                file_nums.append(int(x[1]))
                if latest_file_name is not None and os.path.basename(file_path) == latest_file_name:
                    file_index = i
            filtered_file_paths.append(file_path)

        latest_file_number = 0 if len(file_nums) == 0 else max(file_nums)
        return latest_file_number, file_index, filtered_file_paths

    @staticmethod
    def _possibly_create_save_dir(absolute_dir) -> (str or None, str or None):
        if not os.path.exists(absolute_dir):
            try:
                os.mkdir(absolute_dir, 0o777)
                log.info(f'Created dir ' + absolute_dir)
            except FileNotFoundError as e:
                trace = str(e) + '\n\t' + traceback.format_exc()
                log.error(trace)
                return None, str(e)
        return absolute_dir, None


class AbstractPersistence(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def description(self) -> (str, str):
        pass

    @abc.abstractmethod
    def get(self, create_domain_dct_object) -> dict:
        pass

    @abc.abstractmethod
    def get_next(self, create_domain_dct_object) -> dict:
        pass

    @abc.abstractmethod
    def get_previous(self, create_domain_dct_object) -> dict:
        pass

    @abc.abstractmethod
    def latest_topic(self) -> list:
        pass

    @abc.abstractmethod
    def save(self, file_pfx: str, data_dict: dict) -> str:
        pass

    @abc.abstractmethod
    def update(self, data_dict: dict) -> (str, str):
        pass

    @abc.abstractmethod
    def delete(self, data_dict: dict) -> (str, str):
        pass

    @abc.abstractmethod
    def topics(self) -> str:
        pass


class FilePersistence(AbstractPersistence):
    file_storage_err_msg = True

    def __init__(self, save_dir: str):
        self._status: str = ''
        try:
            absolute_dir = FilePersistence._find_absolute_dir(save_dir)
            self._latest_file_name: str = FilePersistence._find_latest_file_name(absolute_dir)
            self._latest_file_prefix, self._file_prefixes = FilePersistence._find_prefixes(save_dir,
                                                                                           self._latest_file_name)
            self._file_storage = JsonFileStorage(absolute_dir, self._latest_file_prefix, self._latest_file_name)
            FilePersistence.file_storage_err_msg = None
        except Exception as e:
            traceback.print_exc()
            FilePersistence.file_storage_err_msg = str(e)

    @property
    def description(self) -> str:
        return self._file_storage.file_description

    @property
    def latest_topic(self) -> str:
        return self._latest_file_prefix

    @property
    def status(self) -> str:
        return self._status

    @property
    def topics(self) -> list:
        return self._file_prefixes

    def get(self, create_domain_object) -> Dict or None:
        if self._file_storage.is_file_list_empty:
            self._status = f'There are no {self._file_storage.file_pfx} files in {self._file_storage.save_dir}'
            return None
        FilePersistence._validate_file_storage()
        data_dict = self._file_storage.read_file()
        domain_object = None if data_dict is None else create_domain_object(data_dict)
        self._status = 'Read quiz file: ' + self._file_storage.file_path
        return domain_object

    def get_next(self, create_domain_dct_object) -> None or Dict:
        self._file_storage.increment_file_index()
        return self.get(create_domain_dct_object)

    def get_previous(self, create_domain_dct_object) -> None or Dict:
        self._file_storage.decrement_file_index()
        return self.get(create_domain_dct_object)

    def reset(self, file_pfx: str) -> None:
        if self._latest_file_prefix != file_pfx:
            self._latest_file_prefix = file_pfx
            self._file_storage.reset_file_prefix(file_pfx)
            self._status = 'Reset file storage: ' + '??' + ';  '

    def save(self, file_pfx: str, data_dict: dict):
        FilePersistence._validate_file_storage()
        self.reset(file_pfx)
        self._file_storage.save_new_file(data_dict)
        self._status = 'Saved quiz file: ' + self._file_storage.file_path

    def update(self, data_dict: dict):
        FilePersistence._validate_file_storage()
        self._file_storage.update_file(data_dict)
        self._status = 'Updated quiz file: ' + self._file_storage.file_path

    def delete(self):
        FilePersistence._validate_file_storage()
        file_path = self._file_storage.file_path
        try:
            self._file_storage.delete_file()
            self._status = 'Deleted quiz file: ' + file_path
        except InvalidOperation as e:
            self._status = str(e)

    def save_latest_file_name(self) -> str or None:
        file_path = self._file_storage.save_dir + "/latest_work.json"
        data_dict = {'LATEST_FILE_NAME': self._file_storage.latest_file_name}
        with open(file_path, "w", encoding='utf8') as f:
            json.dump(data_dict, f, ensure_ascii=False, sort_keys=False, indent=0)

    @staticmethod
    def _find_prefixes(save_dir: str, latest_file_name: str) -> (str, list):
        absolute_dir = FilePersistence._find_absolute_dir(save_dir)
        prefix = None
        prefixes = FilePersistence._find_file_prefixes(absolute_dir)
        if latest_file_name is not None:
            prefix = re.split(r'[.\-]', latest_file_name)[0]
        if prefix is None and len(prefixes) > 0:
            prefix = prefixes[0]
        if prefix is None:
            prefix = 'quiz'
        if len(prefixes) == 0:
            prefixes = [prefix]
        if prefix not in prefixes:
            raise ValueError(f'file prefix={prefix}, not in {prefixes}')
        return prefix, prefixes

    @staticmethod
    def _validate_file_storage():
        if FilePersistence.file_storage_err_msg is not None:
            raise Exception(FilePersistence.file_storage_err_msg)

    @staticmethod
    def _find_absolute_dir(dir_path: str) -> str:
        absolute_dir = dir_path
        if dir_path.startswith("./"):
            absolute_dir = os.path.dirname(__file__) + absolute_dir[1:]
        absolute_dir = os.path.abspath(absolute_dir)
        if log.isEnabledFor(logging.DEBUG):
            log.debug(f'absolute_dir={absolute_dir}')
        return absolute_dir

    @staticmethod
    def _find_latest_file_name(absolute_dir: str) -> str or None:
        path = absolute_dir + "/latest_work.json"
        if os.path.exists(path):
            with open(path) as f:
                latest_work = json.load(f)
            return latest_work['LATEST_FILE_NAME']
        else:
            return None

    @staticmethod
    def _find_file_prefixes(absolute_dir: str) -> list:
        prefixes = []
        if os.path.exists(absolute_dir):
            for file in sorted(os.listdir(absolute_dir)):
                if file == 'latest_work.json':
                    continue
                if file.endswith('.json'):
                    prefix = re.split(r'[.\-]', file)[0]
                    if prefix not in prefixes:
                        prefixes.append(prefix)
        return prefixes
