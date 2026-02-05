interface SectionsHeaderProps {
    title: string;
    number: string;
}

export const SectionsHeader = ({ title, number }: SectionsHeaderProps) => {
    return (
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-start gap-4">
                <div className="h-16 w-16 rounded-xl bg-primary/10 flex items-center justify-center text-primary">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 6H20M4 12H20M4 18H14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
                <div>
                    <h1 className="text-3xl font-black tracking-tight text-base-content">{title}</h1>
                    <p className="text-sm font-mono text-base-content/50 mt-1">Number: {number}</p>
                </div>
            </div>
        </div>
    );
};