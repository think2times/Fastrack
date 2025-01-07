package flume.demo;

import java.util.List;
import org.apache.commons.codec.Charsets;
import org.apache.flume.Context;
import org.apache.flume.Event;
import org.apache.flume.interceptor.Interceptor;

/**
 * 自定义拦截器类，修改event body体，将本机IP添加到event body体的前面
 */
public class MyFlumeInterceptor implements Interceptor {

    private String hostIP = null;// 自定义属性 hostIP

    // 私有构造函数，仅在内部类MyBuilder中可以对其实例化
    private MyFlumeInterceptor(String hostIP) {
        this.hostIP = hostIP;
    }

    // 修改event的body体
    public Event intercept(Event event) {
        StringBuilder builder = new StringBuilder();
        // 获得body体字节数组
        byte[] byteBody = event.getBody();
        // 将body体转为字符串
        String body = new String(byteBody, Charsets.UTF_8);
        // 拼接IP与body体，形成新body
        builder.append("ip:" + hostIP);
        builder.append(";body:" + body);
        byte[] newBody = builder.toString().trim().getBytes();
        // 重新设置body体
        event.setBody(newBody);
        System.out.println("拼接后的body信息:" + builder.toString().trim());
        return event;
    }

    public List<Event> intercept(List<Event> events) {
        for (Event event : events) {
            intercept(event);
        }
        return events;
    }

    /**
     * 定义内部类MyBuilder，用于构建自定义拦截器类MyFlumeInterceptor的实例，
     * 并获取Flume配置文件中自定义的拦截器属性值，将值传给自定义类MyFlumeInterceptor
     */
    public static class MyBuilder implements Interceptor.Builder {

        private String hostIP = null;

        public void configure(Context context) {
            // 获取Flume配置文件中设置的自定义属性值，字符串“hostIP”需与配置文件中设置的属性hostIP一致
            String hostIP = context.getString("hostIP");
            this.hostIP = hostIP;
        }

        public Interceptor build() {
            // 实例化自定义拦截器类并传入自定义属性
            return new MyFlumeInterceptor(hostIP);
        }
    }

    public void close() {
    }

    public void initialize() {
    }

}
