import {
  Stethoscope,
  Plus,
  MessageSquare,
  BookOpen,
  Pill,
  Microscope,
  Image,
  Settings,
} from "lucide-react";

function Sidebar({ clearChat }) {
  return (
    <aside className="sidebar">

      <div>
        <h2>
          <Stethoscope size={24} />
          MediAgent
        </h2>

        <p className="sidebar-version">
          Clinical Intelligence Platform
        </p>
      </div>

      <button onClick={clearChat}>
        <Plus size={18} />
        New Clinical Session
      </button>

      <nav className="sidebar-nav">

        <div className="nav-section">
          <span className="nav-title">Workspace</span>

          <button className="nav-item active">
            <MessageSquare size={18} />
            Clinical Chat
          </button>

          <button className="nav-item">
            <BookOpen size={18} />
            Literature Review
          </button>

          <button className="nav-item">
            <Pill size={18} />
            Drug Intelligence
          </button>

          <button className="nav-item">
            <Microscope size={18} />
            Research
          </button>

          <button className="nav-item">
            <Image size={18} />
            Medical Imaging
          </button>

        </div>

        <div className="nav-bottom">

          <button className="nav-item">
            <Settings size={18} />
            Settings
          </button>

        </div>

      </nav>

    </aside>
  );
}

export default Sidebar;