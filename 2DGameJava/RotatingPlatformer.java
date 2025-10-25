
import javax.swing.*;
import java.awt.*;

public class RotatingPlatformer {
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            JFrame frame = new JFrame("Rotating Rectangle Platformer");
            GamePanel gamePanel = new GamePanel();

            frame.add(gamePanel);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

            gamePanel.startGame();
        });
    }
}
