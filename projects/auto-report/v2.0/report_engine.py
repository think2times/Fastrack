from database_streamer import DatabaseStreamer

class ReportEngine:
    def __init__(self, streamer: DatabaseStreamer):
        self.streamer = streamer

    def run(self, observers: list):
        # 核心特性：无论数据量大小，代码逻辑只有这一套
        for chunk in self.streamer:
            for obs in observers:
                obs.on_next(chunk)
        
        # 收集结果
        return {type(o).__name__: o.on_completed() for o in observers}
