function ConfidenceBar({ confidence }) {

    const percentage = Math.round(confidence);

    return (

        <div className="mt-4">

            <p className="font-semibold mb-2">

                Confidence Score

            </p>

            <div className="w-full bg-gray-200 rounded-full h-4">

                <div

                    className="bg-green-600 h-4 rounded-full"

                    style={{

                        width: `${percentage}%`

                    }}

                />

            </div>

            <p className="mt-2">

                {percentage}%

            </p>

        </div>

    );

}

export default ConfidenceBar;