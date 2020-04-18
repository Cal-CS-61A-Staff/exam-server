import React, { useState } from "react";
import { getToken } from "./auth";
import FailText from "./FailText";
import LoadingButton from "./LoadingButton";
import post from "./post";

export default function ExamDownloader({ exam, onReceive }) {
    const [loading, setLoading] = useState(false);

    const [failText, setFailText] = useState("");

    const download = async () => {
        setLoading(true);
        setFailText("");

        const ret = await post("get_exam", { token: getToken(), exam });
        if (!ret.ok) {
            setFailText(`
                The exam server failed with error ${ret.status}. Please try again. 
            `);
        }

        try {
            const data = await ret.json();

            if (!data.success) {
                setFailText(`
                    The exam server responded but did not produce a valid exam. Please try again. 
                `);
            } else {
                onReceive(data);
            }
        } catch {
            setFailText("The web server returned invalid JSON. Please try again.");
        }

        setLoading(false);
    };

    return (
        <>
            <LoadingButton onClick={download} disabled={loading} loading={loading}>
                Generate Exam
            </LoadingButton>
            <FailText text={failText} />
        </>
    );
}
