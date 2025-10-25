
import java.awt.*;

public class Platform {
    private int x, y, width, height;

    public Platform(int x, int y, int width, int height) {
        this.x = x;
        this.y = y;
        this.width = width;
        this.height = height;
    }

    public Rectangle getBounds() {
        return new Rectangle(x, y, width, height);
    }

    public void draw(Graphics2D g2d) {
        // Draw platform
        g2d.setColor(new Color(101, 67, 33)); // Brown
        g2d.fillRect(x, y, width, height);

        // Draw border
        g2d.setColor(new Color(80, 50, 20));
        g2d.setStroke(new BasicStroke(2));
        g2d.drawRect(x, y, width, height);

        // Draw grass on top
        g2d.setColor(new Color(34, 139, 34));
        g2d.fillRect(x, y, width, 8);
    }
}
