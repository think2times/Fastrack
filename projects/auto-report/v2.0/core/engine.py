from streamer import DataStreamer

class ReportEngine:
    def __init__(self, streamer: DataStreamer):
        self.streamer = streamer

    def run(self, streamer, observers):
        # streamer 产生的是 (idx, df) 元组
        for idx, chunk in streamer:
            for obs in observers:
                obs.on_next(idx, chunk)
        
        # 汇总结果
        return {type(o).__name__: o.on_completed() for o in observers}
