from config.config import REPORTS

from core.engine import ReportEngine
from core.streamer import DataStreamer
from core.observers import AuditObserver, ExportObserver


class TaskFactory:
    def __init__(self, conn, sub_com, month):
        self.conn = conn
        self.sub_com = sub_com
        self.month = month

    def create_task(self, report_id):
        # 1. 从配置字典中获取配置 (假设已导入报表字典)
        cfg = REPORTS.get(report_id)
        
        # 2. 核心：极简参数处理逻辑
        if cfg is None:
            # 抛出更友好的错误，告诉你哪个报表编号没配对
            raise ValueError(f"报表 ID '{report_id}' 未在配置文件中定义，请检查 report_cfg.py")
        # 如果配置里写了 lambda，就用 lambda；否则根据 params_extra 补空位
        if 'params' in cfg:
            final_params = cfg['params'](self.sub_com, self.month)
        else:
            # 默认 [sub, month]，根据配置补 ['', ''] 等
            extra_count = cfg.get('params_extra', 0)
            final_params = [self.sub_com, self.month] + ([''] * extra_count)

        # 3. 实例化流对象
        streamer = DataStreamer(self.conn, cfg['proc_name'], final_params)
        
        # 4. 组装观察者 (这里可以根据 cfg 里的 group_by 自动判断实例化哪个类)
        observers = self._build_observers(cfg)
        
        return ReportEngine(streamer), observers

    def _build_observers(self, cfg):
        obs_list = []
        cursor_indices = [0]  # 默认只有一个游标索引为 0
        if cfg.get('multi_cursors', 1) > 1:
            cursor_indices = [i for i in range(cfg['multi_cursors'])]

        # 添加审计观察者
        obs_list.append(AuditObserver(cursor_indices))
        # 添加导出观察者
        obs_list.append(ExportObserver(cfg['file_name'], cfg['columns_map']))
        return obs_list
