import { useRef, useState } from "react";
import "./Camera.css";

function Camera() {
  const videoRef = useRef(null);

  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  // Test events for now
  const events = [
    {
      id: 1,
      time: 10,
      type: "Motion",
    },
    {
      id: 2,
      time: 25,
      type: "Intrusion",
    },
    {
      id: 3,
      time: 40,
      type: "Intrusion",
    },
  ];

  // Update current video time
  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  // Get video duration
  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  // Click on timeline
  const handleTimelineClick = (event) => {
    if (!videoRef.current || !duration) return;

    const rect = event.currentTarget.getBoundingClientRect();

    const clickPosition = event.clientX - rect.left;

    const percentage = clickPosition / rect.width;

    const newTime = percentage * duration;

    videoRef.current.currentTime = newTime;

    setCurrentTime(newTime);
  };

  // Jump to an event
  const jumpToEvent = (time) => {
    if (videoRef.current) {
      videoRef.current.currentTime = time;
      videoRef.current.play();

      setCurrentTime(time);
    }
  };

  // Format seconds into MM:SS
  const formatTime = (seconds) => {
    if (!seconds || isNaN(seconds)) {
      return "00:00";
    }

    const minutes = Math.floor(seconds / 60);

    const secs = Math.floor(seconds % 60);

    return `${minutes.toString().padStart(2, "0")}:${secs
      .toString()
      .padStart(2, "0")}`;
  };

  return (
    <div className="camera-page">

      {/* Camera Header */}

      <div className="camera-header">

        <div>
          <h1>Camera 01</h1>
          <p>East Gate</p>
        </div>

        <div className="camera-status">
          ● ONLINE
        </div>

      </div>


      {/* Video */}

      <div className="video-container">

        <video
          ref={videoRef}
          className="video-player"
          controls
          src="/camera01.mp4"
          onTimeUpdate={handleTimeUpdate}
          onLoadedMetadata={handleLoadedMetadata}
        >
          Your browser does not support video playback.
        </video>

      </div>


      {/* Timeline Section */}

      <div className="timeline-section">

        <div className="timeline-header">

          <span>Recorded Timeline</span>

          <span>
            {formatTime(currentTime)} / {formatTime(duration)}
          </span>

        </div>


        {/* Timeline */}

        <div
          className="timeline"
          onClick={handleTimelineClick}
        >

          {/* Progress */}

          <div
            className="timeline-progress"
            style={{
              width: duration
                ? `${(currentTime / duration) * 100}%`
                : "0%",
            }}
          />


          {/* Event Markers */}

          {events.map((event) => {

            const position = duration
              ? (event.time / duration) * 100
              : 0;

            return (
              <button
                key={event.id}
                className={`event-marker ${
                  event.type === "Intrusion"
                    ? "intrusion-marker"
                    : "motion-marker"
                }`}
                style={{
                  left: `${position}%`,
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  jumpToEvent(event.time);
                }}
                title={`${event.type} - ${formatTime(event.time)}`}
              />
            );

          })}

        </div>


        {/* Timeline Labels */}

        <div className="timeline-labels">

          <span>00:00</span>

          <span>{formatTime(duration / 2)}</span>

          <span>{formatTime(duration)}</span>

        </div>


        {/* Events */}

        <div className="event-list">

          <h3>Detected Events</h3>

          {events.map((event) => (

            <button
              key={event.id}
              className="event-item"
              onClick={() => jumpToEvent(event.time)}
            >

              <span
                className={
                  event.type === "Intrusion"
                    ? "event-dot intrusion"
                    : "event-dot motion"
                }
              />

              <div>

                <strong>
                  {event.type}
                </strong>

                <p>
                  Camera 01 • {formatTime(event.time)}
                </p>

              </div>

            </button>

          ))}

        </div>

      </div>

    </div>
  );
}

export default Camera;