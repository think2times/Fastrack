from config.config import CALC_CONFIG, REPORTS_CONFIG

from core.engine import ReportEngine
from core.streamer import DataStreamer
from core.observers import AuditObserver, ExportObserver


class TaskFactory:
    def __init__(self, conn, sub_com, month):
        self.conn = conn
        self.sub_com = sub_com
        self.month = month

    def create_task(self, report_id):
        # 1. 从配置字典中获取配置
        cfg = REPORTS_CONFIG.get(report_id)
        
        # 2. 核心：极简参数处理逻辑
        if cfg is None:
            # 抛出更友好的错误，告诉你哪个报表没有配置
            raise ValueError(f"报表 ID '{report_id}' 未在配置文件中定义，请检查 config/config.py")
        # 如果配置里写了 lambda，就用 lambda；否则根据 params_extra 补空位
        if 'params' in cfg:
            final_params = cfg['params'](self.sub_com, self.month)
        else:
            # 默认 [sub, month]，根据配置补 ['', ''] 等
            extra_count = cfg.get('params_extra', 0)
            final_params = [self.sub_com, self.month] + ([''] * extra_count)

        # 3. 实例化流对象
        calc_func = CALC_CONFIG.get(report_id)  # 获取对应的计算函数

        # 4. 创建带计算逻辑的引擎
        engine = ReportEngine(calc_func=calc_func)

        streamer = DataStreamer(self.conn, cfg['proc_name'], final_params)

        # 5. 组装观察者 (这里可以根据 cfg 里的 group_by 自动判断实例化哪个类)
        observers = self._build_observers(cfg)

        return engine, streamer, observers

    def _build_observers(self, cfg):
        obs_list = []

        # 添加审计观察者
        obs_list.append(AuditObserver(cfg))

        # 添加导出观察者
        obs_list.append(ExportObserver(cfg))
        return obs_list
