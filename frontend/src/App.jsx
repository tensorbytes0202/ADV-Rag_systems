import Navbar from "./components/Navbar";
import UploadSection from "./components/UploadSection";
import QuerySection from "./components/QuerySection";
import DocumentSelector from "./components/DocumentSelector";

function App() {

  return (

    <div className="min-h-screen bg-gray-100">

      <Navbar />

      <div className="max-w-5xl mx-auto p-6">

        <UploadSection />

        <DocumentSelector />

        <QuerySection />

      </div>

    </div>

  );
}

export default App;