#include <X11/Xlib.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>

//            Bat Deg | Bat | CPU Load         | Date       Time
char name[] = "xx.xx% | x.xx, x.xx, x.xx | xxxx-xx-xx xx:xx:xx";

// return 8 chars
void charge(char *buf) {
  FILE *charge_file = fopen("/sys/class/power_supply/BAT0/charge_now", "r");
  FILE *charge_full_file =
      fopen("/sys/class/power_supply/BAT0/charge_full", "r");

  unsigned int cap = 0;
  char cap_str[10];
  fgets(cap_str, 10, charge_full_file);

  unsigned int charge = 0;
  char charge_str[10];
  fgets(charge_str, 10, charge_file);
  pclose(charge_file);
  pclose(charge_full_file);

#pragma unroll
  for (int i = 0; i < 10; i++) {
    if (cap_str[i] >= '0' && cap_str[i] <= '9') {
      cap = cap * 10 + (cap_str[i] - '0');
    }
    if (charge_str[i] >= '0' && charge_str[i] <= '9') {
      charge = charge * 10 + (charge_str[i] - '0');
    }
  }

  unsigned int charge_percent = charge * 1000 / ( cap / 10 );
  char *charge_percent_str[5];
  printf("%d\n", charge_percent);
  sprintf(buf, "%02d.%02d\% | ", charge_percent / 100, charge_percent % 100);
}

void date(char *buf, short centiseconds) {
  time_t t = time(NULL);
  struct tm tm = *localtime(&t);

  sprintf(buf, "%04d-%02d-%02d %02d:%02d:%02d.%02d", tm.tm_year + 1900,
          tm.tm_mon + 1, tm.tm_mday, tm.tm_hour, tm.tm_min, tm.tm_sec, centiseconds);
}

int main() {
  Display *dpy = XOpenDisplay(":0");
  const int screen = DefaultScreen(dpy);
  const Window root = RootWindow(dpy, screen);
  while (1) {
    charge(name);

    #pragma unroll
    for (int i = 0; i < 100; i++) {
      date(name + 9, i);
      printf("%s\n", name);
      usleep(10000);
      XStoreName(dpy, root, name);
    }

  }
  return 0;
}

