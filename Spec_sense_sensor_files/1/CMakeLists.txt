cmake_minimum_required(VERSION 2.8.12)
project(NotificationDemo CXX)

add_subdirectory(kaa)
add_subdirectory(convenience)
add_executable(kaa-app main.cpp )

target_link_libraries(kaa-app kaacpp rtlsdr)
