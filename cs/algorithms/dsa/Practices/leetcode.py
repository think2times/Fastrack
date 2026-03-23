from typing import List
import sys, pygame


class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        lo = 0
        hi = len(nums)
        while(lo < hi):
            mid = lo + ((hi - lo) >> 1)
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                hi = mid
            else:
                lo = mid + 1
        return lo
    
    def removeElement(self, nums: List[int], val: int) -> int:
        lo = 0
        hi = len(nums)-1
        while (lo <= hi):
            if nums[lo] == val:
                nums[lo] = nums[hi]
                hi -= 1
            else:
                lo += 1
        return lo


if __name__ == "__main__":
    pygame.init()

    size = width, height = 1366, 768
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    ball = pygame.image.load("intro_ball.gif")
    ballrect = ball.get_rect()
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: 
                sys.exit()
        
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
        
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
