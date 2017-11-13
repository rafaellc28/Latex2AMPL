set STUDENTS;

set COURSES;

param credits{c in COURSES}, >= 0;

param schedules{s in STUDENTS, c in COURSES} binary;

param loads{s in STUDENTS}, := sum{c in COURSES}schedules[s,c] * credits[c];





